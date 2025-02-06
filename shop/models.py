from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse
from django.conf import settings





# Abstract model for timestamp fields
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created` and `modified` fields.
    """
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True



# Product Category
class Category(models.Model):
    """
    Represents product categories.
    """
    name = models.CharField("Product Category", max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('name',)  # Order by name alphabetically
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # Return the revenue of products on shelves
    def total_selling_price(self):
        return self.products.aggregate(total_price=Sum('selling_price'))['total_price'] or 0

    # Count the number of products are on shelves
    def count_products_on_category(self):
        return self.products.count()


    


# Shelf Model
class Shelf(TimeStampedModel):
    """
    Represents shelves where products are stored.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    # Return the revenue of products on shelves
    def total_selling_price(self):
        return self.products.aggregate(total_price=Sum('selling_price'))['total_price'] or 0

    # Count the number of products are on shelves
    def count_products_on_shelf(self):
        return self.products.count()


# Product Model
class Product(TimeStampedModel):
    """
    Represents individual products in the inventory.
    """
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150, db_index=True)
    image = models.ImageField(upload_to="ProductImages", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    barcode = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    shelf = models.ForeignKey(
        Shelf,
        verbose_name="Shelf",
        related_name="products",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    quantity_in_stock = models.BigIntegerField()
    expiry_date = models.DateField(blank=True, null=True)
    unit_of_measurement = models.CharField(
        max_length=20,
        choices=[
            ('pcs', 'Pieces'),
            ('kg', 'Kilograms'),
            ('liters', 'Liters'),
        ],
        default='pcs',
    )

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']), 
        ]

    def get_absolute_url(self):
        return reverse('product_app:product-detail',
                        args=[self.id, self.slug])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # Validate the form
    def clean(self):
        # Ensure quantity_in_stock is not None before comparing
        if self.quantity_in_stock is not None and self.quantity_in_stock < 0:
            raise ValidationError("Quantity in stock cannot be negative.")

        # Ensure expiry_date is not None before comparing with today's date
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError("Expiry date cannot be in the past.")

        # Ensure cost_price and selling_price are not None before comparison
        if self.cost_price is not None and self.selling_price is not None:
            if self.selling_price <= self.cost_price:
                raise ValidationError("Selling price must be greater than the cost price.")


    def increase_stock(self, quantity):
        previous_quantity = self.quantity_in_stock
        self.quantity_in_stock += quantity
        self.save()
        StockHistory.objects.create(
            product=self,
            change_type='add',
            quantity_changed=quantity,
            previous_quantity=previous_quantity,
            new_quantity=self.quantity_in_stock
        )

    def decrease_stock(self, quantity):
        if quantity > self.quantity_in_stock:
            raise ValueError("Insufficient stock!")
        previous_quantity = self.quantity_in_stock
        self.quantity_in_stock -= quantity
        self.save()
        StockHistory.objects.create(
            product=self,
            change_type='remove',
            quantity_changed=quantity,
            previous_quantity=previous_quantity,
            new_quantity=self.quantity_in_stock
        )


    # Stock Levels `Low stocks`
    LOW_STOCK_THRESHOLD = 100  # Set a threshold for low stock

    def get_stock_status(self):
        """
        Returns the stock status based on the quantity_in_stock.
        """
        if self.quantity_in_stock <= 0:
            return "Out of Stock"
        elif self.quantity_in_stock <= self.LOW_STOCK_THRESHOLD:
            return "Low Stock"
        else:
            return "In Stock"


    # Return Total Balance of selling and cost price
    @classmethod
    def get_total_balances(cls):
        total_cost_price = cls.objects.filter(quantity_in_stock__gt=1).aggregate(Sum('cost_price'))['cost_price__sum'] or 0
        total_selling_price = cls.objects.filter(quantity_in_stock__gt=1).aggregate(Sum('selling_price'))['selling_price__sum'] or 0
        return {
            'total_cost_price': total_cost_price,
            'total_selling_price': total_selling_price
        }
    

    def __str__(self):
        return self.name




# TODO  This most be deleted
class StockHistory(models.Model):
    product = models.ForeignKey(Product, related_name='stock_history', on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=[('add', 'Added'), ('remove', 'Removed')])
    quantity_changed = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity_changed}) on {self.timestamp}"



# Stock Adjustment 
class StockAdjustment(TimeStampedModel):
    """
    Logs stock adjustments (increase or decrease).
    """
    INCREASE = "increase"
    DECREASE = "decrease"
    
    ADJUSTMENT_CHOICES = [
        (INCREASE, "Increase"),
        (DECREASE, "Decrease"),
    ]

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="adjustments")
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()

    def apply_adjustment(self):
        """Adjusts the product stock and saves the record."""
        if self.adjustment_type == self.INCREASE:
            self.product.quantity_in_stock += self.quantity
        elif self.adjustment_type == self.DECREASE:
            self.product.quantity_in_stock = max(0, self.product.quantity_in_stock - self.quantity)  # Prevent negative stock
        self.product.save()
        self.save()  # Log the adjustment record

    def __str__(self):
        return f"{self.adjustment_type.capitalize()} {self.quantity} of {self.product.name}"
    


    
# Adjustment History
class StockAdjustmentHistory(models.Model):
    ADJUSTMENT_TYPES = (
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    )

    product = models.ForeignKey(Product, related_name="adjustment_history", on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    adjusted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming you're using Django's built-in User model
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type.capitalize()} {self.quantity} of {self.product.name} on {self.date}"

    class Meta:
        verbose_name = "Stock Adjustment History"
        verbose_name_plural = "Stock Adjustment Histories"
        ordering = ['-date']



# Stock Transfer
class StockTransfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    source_shelf = models.ForeignKey(Shelf, related_name='source_shelf', on_delete=models.SET_NULL, null=True)
    destination_shelf = models.ForeignKey(Shelf, related_name='destination_shelf', on_delete=models.SET_NULL, null=True)
    quantity_transferred = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, null=True, blank=True)
    # transferred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.quantity_transferred} {self.product.name} from {self.source_shelf.name} to {self.destination_shelf.name}"