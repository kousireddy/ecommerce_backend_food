from rest_framework import serializers
from .models import Review
from products.models import Product

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # shows username

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'reviews']