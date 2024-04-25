from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.api.views.views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': "list", "post": "create"}), name='user-list'),
    path('users/<str:username>/', UserViewSet.as_view({'get': "retrieve", "patch": "partial_update", "delete": "destroy"}),
         name='user-detail'),
    # token api
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]