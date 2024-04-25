from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Djote.utils.view_utils import ReadWriteSerializerViewMixin, StandardResultsSetPagination
from user.api.serializers.serializers import UserReadSerializer, UserWriteSerializer
from user.filtersets import UserFilterSet
from user.models import AuthUser


class UserViewSet(viewsets.ModelViewSet, ReadWriteSerializerViewMixin):
    read_serializer = UserReadSerializer
    write_serializer = UserWriteSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = UserFilterSet
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["username"]

    def get_queryset(self):
        return AuthUser.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), username=self.kwargs.get("username"))

    def destroy(self, request, *args, **kwargs):
        instance: AuthUser = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
