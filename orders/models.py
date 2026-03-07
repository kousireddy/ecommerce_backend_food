from django.db import models
from users.models import User
from products.models import Product


class Order(models.Model):

    STATUS = (
        ("pending","Pending"),
        ("processing","Processing"),
        ("shipped","Shipped"),
        ("delivered","Delivered"),
    )

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="processing"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)