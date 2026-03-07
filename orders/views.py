from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from cart.models import UserCart, UserCartItem
from .models import Order, OrderItem
from users.models import User
from .serializers import OrderSerializer

class CheckoutView(APIView):

    def post(self, request, user_id):

        cart = get_object_or_404(UserCart, user_id=user_id)
        cart_items = UserCartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = 0

        # Create order with 'processing' status
        order = Order.objects.create(
            user_id=user_id,
            total_price=0,
            status="processing",
            payment_status="paid"
        )

        # Create order items
        order_items_bulk = []
        for item in cart_items:
            order_items_bulk.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            )
            total += item.product.price * item.quantity

        OrderItem.objects.bulk_create(order_items_bulk)

        order.total_price = total
        order.save()

        cart_items.delete()

        serializer = OrderSerializer(order)

        return Response({
            "message": "Order placed successfully",
            "order": serializer.data
        })
    

class UserOrdersView(APIView):

    def get(self, request, user_id):

        orders = Order.objects.filter(user_id=user_id).order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class AdminOrdersView(APIView):

    def get(self, request, user_id):

        user = get_object_or_404(User, id=user_id)

        if not user.is_admin:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        orders = Order.objects.all().order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class UpdateOrderStatusView(APIView):

    def put(self, request, order_id):

        order = get_object_or_404(Order, id=order_id)

        status_value = request.data.get("status")

        if status_value not in dict(Order.STATUS).keys():
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        return Response({"message": "Order status updated"})