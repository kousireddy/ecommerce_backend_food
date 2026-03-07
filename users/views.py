from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserRegisterSerializer,LoginSerializer
from .models import User
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, LoginSerializer


class VerifyOTPView(APIView):
    def post(self, request):

        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)

            if user.otp == otp:
                user.is_verified = True
                user.otp = None
                user.save()

                return Response(
                    {"message": "Email verified successfully"},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            print("Generated OTP:", otp)

            # Send email
            send_mail(
                subject="Email Verification OTP",
                message=f"Hello {user.username}, your OTP for email verification is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            if not user.is_verified:
                return Response(
                    {"error": "Please verify your email first"},
                    status=400
                )
            
            # Generate JWT Tokens
            refresh = RefreshToken()
            refresh["user_id"] = user.id
            refresh["username"] = user.username

            access = refresh.access_token

            return Response(
                {
                    "message": "Login successful",
                    "access_token": str(access),
                    "refresh_token": str(refresh),
                    "user": UserSerializer(user).data,
                    "is_admin": user.is_admin
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserListView(APIView):
    
    def get(self, request):
        def get(self, request):
            if not request.user.is_admin:
                return Response({"error":"Admin only"}, status=403)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer