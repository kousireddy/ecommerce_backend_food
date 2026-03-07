from django.urls import path
from .views import CheckoutView,UserOrdersView,AdminOrdersView,UpdateOrderStatusView

urlpatterns = [

path("checkout/<int:user_id>/",CheckoutView.as_view()),

path("my-orders/<int:user_id>/",UserOrdersView.as_view()),

path("admin-orders/<int:user_id>/",AdminOrdersView.as_view()),

path("update-status/<int:order_id>/",UpdateOrderStatusView.as_view()),

]