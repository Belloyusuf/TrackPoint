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


# Customer
class Customer(TimeStampedModel):
    """" Customer's model """
    CUSTOMERS_TYPE = [
        ("Regular", "Regular"),
        ("Customer 2", "Customer 2"),
        ("Customer 3", "Customer 3"),
    ]
    name = models.CharField(("Customer Name"), max_length=30)
    customer_type = models.CharField(choices=CUSTOMERS_TYPE, max_length=50)
    
