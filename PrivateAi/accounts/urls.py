from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from accounts.views import RegisterView, NewPasswordView, ForgetPassword

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),

    path("register/", RegisterView.as_view(), name="register"),
    path("new_password/", NewPasswordView.as_view(), name="new_password"),
    path("forget_password/", ForgetPassword.as_view(), name="forget_password"),
]
