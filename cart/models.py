from django.db import models
from users.models import User
from products.models import Product


class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserCartItem(models.Model):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name