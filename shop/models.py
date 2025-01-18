from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone





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
    quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2)
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
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if self.quantity_in_stock < 0:
            raise ValidationError("Quantity in stock cannot be negative.")
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError("Expiry date cannot be in the past.")

    def increase_stock(self, quantity):
        self.quantity_in_stock += quantity
        self.save()


    def decrease_stock(self, quantity):
        if quantity > self.quantity_in_stock:
            raise ValueError("Insufficient stock!")
        self.quantity_in_stock -= quantity
        self.save()

    def __str__(self):
        return self.name
