from django.db import models
from shop.models import Product

# from django.contrib.auth.models import User

class Order(models.Model):
    # Customer Type Choices
    WALK_IN = "Walk-in"
    REGULAR = "Regular"
    WHOLESALE = "Wholesale"
    B2B = "B2B"
    SUBSCRIPTION = "Subscription"

    CUSTOMERS_TYPE = [
        (WALK_IN, "Walk-in Customer"),
        (REGULAR, "Regular Customer"),
        (WHOLESALE, "Wholesale Customer"),
        (B2B, "B2B Customer"),
        (SUBSCRIPTION, "Subscription Customer"),
    ]

    # Payment Methods
    PAYMENT_METHOD = [
        ("Cash", "Cash"),
        ("Transfer", "Transfer"),
        ("POS", "POS")
    ]

    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_type = models.CharField(choices=CUSTOMERS_TYPE, default=WALK_IN, max_length=50)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default="Cash", max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id} - {self.customer_type}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only reduce stock for new orders
            self.product.quantity_in_stock -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Item {self.id} - {self.product.name} ({self.quantity})'

    def get_cost(self):
        return self.price * self.quantity
