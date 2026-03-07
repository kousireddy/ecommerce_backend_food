from django.urls import path
from .views import ProductReviewView,AddReviewView,AllReviewsView

urlpatterns = [
    path("product-reviews/<int:product_id>/", ProductReviewView.as_view()),
    path("add-review/", AddReviewView.as_view(), name="add-review"),
    path("all-reviews/", AllReviewsView.as_view(), name="all-reviews"),
]