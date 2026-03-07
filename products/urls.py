from django.urls import path
from .views import ProductListView, CategoryListView, AddProductView,AddCategoryView,CategoryProductView,UserProductView,CategoryProductsWithReviews,SingleProductView,DeleteProductView,UpdateStockView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("products/", ProductListView.as_view()),
    path("add-product/", AddProductView.as_view()),
    path("add-category/", AddCategoryView.as_view()),
    path("category-products/", CategoryProductView.as_view()),
    path("user-products/", UserProductView.as_view()),
    path("category-products-with-reviews/", CategoryProductsWithReviews.as_view(), name="category-products-with-reviews"),
    path("<int:product_id>/", SingleProductView.as_view(), name="single-product"),
    path("delete/<int:product_id>/",DeleteProductView.as_view()),
    path("update-stock/<int:product_id>/", UpdateStockView.as_view()),
]