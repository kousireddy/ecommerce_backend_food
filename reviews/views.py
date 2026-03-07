from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from users.models import User
from products.models import Product
from products.serializers import ProductSerializer

class ProductReviewView(APIView):

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class AddReviewView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user")
            product_id = request.data.get("product")
            rating = request.data.get("rating")
            comment = request.data.get("comment")

            rating = int(rating)

            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)

            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment
            )

            return Response({"message": "Review submitted"}, status=201)
        
     
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class AllReviewsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)