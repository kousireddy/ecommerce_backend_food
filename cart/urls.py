from django.urls import path
from .views import AddToCartView, CartView, RemoveCartItemView,UpdateCartQuantityView

urlpatterns = [
    path('add/', AddToCartView.as_view()),
    path('items/<int:user_id>/', CartView.as_view()),
    path('remove/<int:id>/', RemoveCartItemView.as_view()),
    path('update-qty/', UpdateCartQuantityView.as_view()),
]