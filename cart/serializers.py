from rest_framework import serializers
from .models import UserCartItem

class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.IntegerField(source="product.price", read_only=True)
    image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = UserCartItem
        fields = [
            "id",
            "product_name",
            "price",
            "quantity",
            "image"
        ]