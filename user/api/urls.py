from django.urls import path

from user.api.views.auth_views import CustomTokenObtainPairView, OTPVerificationView, CustomLogoutView
from user.api.views.views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': "list", "post": "create"}), name='user-list'),
    path('users/<str:username>/', UserViewSet.as_view({'get': "retrieve", "patch": "partial_update", "delete": "destroy"}),
         name='user-detail'),
    # token api
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('otp/verify/', OTPVerificationView.as_view(), name='otp_verify'),
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),
]