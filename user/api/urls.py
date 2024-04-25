from django.urls import path

from user.api.views.views import UserViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view({'get': "list", "post": "create"}), name='user-list'),
    path('user/<str:username>/', UserViewSet.as_view({'get': "retrieve", "patch": "partial_update", "delete": "destroy"}),
         name='user-detail'),
]