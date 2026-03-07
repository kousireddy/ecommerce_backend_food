from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from reviews.serializers import ReviewSerializer
from rest_framework.parsers import MultiPartParser,FormParser

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class AddCategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AddProductView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CategoryProductView(APIView):

    def get(self, request):

        categories = Category.objects.all()

        result = []

        for category in categories:

            products = Product.objects.filter(category=category)

            result.append({
                "category": category.name,
                "products": ProductSerializer(products, many=True).data
            })

        return Response(result)
    
class UserProductView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        result = []

        for category in categories:
            products = Product.objects.filter(category=category)
            products_data = []
            for product in products:
                products_data.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "in_stock": product.in_stock,
                    "image": request.build_absolute_uri(product.image.url) if product.image else None,
                    "reviews": ReviewSerializer(product.reviews.all(), many=True).data
                })
            result.append({
                "category": category.name,
                "products": products_data
            })
        return Response(result)

class CategoryProductsWithReviews(APIView):
    def get(self, request):
        categories = Category.objects.all()
        result = []

        for category in categories:
            products = Product.objects.filter(category=category)
            products_data = []

            for product in products:
                reviews = product.reviews.all()  # related_name="reviews"
                products_data.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "in_stock": product.in_stock,
                    "image": request.build_absolute_uri(product.image.url) if product.image else None,
                    "reviews": ReviewSerializer(reviews, many=True).data
                })

            result.append({
                "id": category.id,
                "category": category.name,
                "products": products_data
            })

        return Response(result)

class SingleProductView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

class DeleteProductView(APIView):

    def delete(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)
            product.delete()

            return Response({
                "message": "Product deleted successfully"
            })

        except Product.DoesNotExist:
            return Response({
                "error": "Product not found"
            }, status=404)
    
class UpdateStockView(APIView):
    def put(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)

            product.in_stock = request.data.get("in_stock")

            product.save()

            return Response({
                "message": "Stock updated"
            })

        except Product.DoesNotExist:
            return Response({
                "error": "Product not found"
            }, status=404)