from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum





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




# Shelf Model
class Shelf(models.Model):
    """
    Represents shelves where products are stored.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
        # index_together = (('id', 'slug'),)

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
        self.quantity_in_stock += quantity
        self.save()


    def decrease_stock(self, quantity):
        if quantity > self.quantity_in_stock:
            raise ValueError("Insufficient stock!")
        self.quantity_in_stock -= quantity
        self.save()


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





    


    