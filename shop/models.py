from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse






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



class StockHistory(models.Model):
    product = models.ForeignKey(Product, related_name='stock_history', on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=[('add', 'Added'), ('remove', 'Removed')])
    quantity_changed = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity_changed}) on {self.timestamp}"




    


    