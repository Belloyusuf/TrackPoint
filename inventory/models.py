from django.db import models


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




# Inventory  Settings
class InventorySetting(TimeStampedModel):
    name = models.CharField(("Inventory Name"), max_length=150)
    logo = models.ImageField(upload_to="InventoryImages", height_field=None, width_field=None, max_length=None)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, null=True, blank=True)
    web_address = models.CharField(max_length=150, null=True, blank=True)
    phone1 = models.CharField(("Phone Number"), max_length=15)
    phone2 = models.CharField(("Phone Number 2"), max_length=15, null=True, blank=True)


    def __str__(self):
        return self.name