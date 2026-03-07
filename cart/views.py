from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserCart,UserCartItem
from .serializers import CartItemSerializer
from products.models import Product
from users.models import User

class AddToCartView(APIView):
    def post(self, request):

        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        cart, created = UserCart.objects.get_or_create(user=user)

        cart_item, created = UserCartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({"message": "Product added to cart"})


class CartView(APIView):

    def get(self, request, user_id):

        user = User.objects.get(id=user_id)

        cart, created = UserCart.objects.get_or_create(user=user)
        items = UserCartItem.objects.filter(cart=cart)

        serializer = CartItemSerializer(items, many=True, context={"request": request})

        total_price = 0
        for item in items:
            total_price += item.product.price * item.quantity

        return Response({
            "items": serializer.data,
            "total_price": total_price
        })

class RemoveCartItemView(APIView):

    def delete(self, request, id):

        item =UserCartItem.objects.get(id=id)
        item.delete()

        return Response({"message":"Item removed"})

class UpdateCartQuantityView(APIView):

    def post(self, request):

        item_id = request.data.get("item_id")
        action = request.data.get("action")

        item = UserCartItem.objects.get(id=item_id)

        if action == "increase":
            item.quantity += 1

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1

        item.save()

        return Response({
            "message": "Quantity updated",
            "quantity": item.quantity
        })