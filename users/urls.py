from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserListView,VerifyOTPView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/<int:user_id>/", ProfileView.as_view()),
    path("list/", UserListView.as_view()),
]