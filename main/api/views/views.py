from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from Djote.utils.view_utils import ReadWriteSerializerViewMixin, StandardResultsSetPagination, IsOTPVerified
from main.filtersets import NoteFilterSet
from main.models import Note
from main.api.serializers.serializer import NoteReadSerializer, NoteWriteSerializer


@extend_schema(tags=["note"])
class NoteViewSet(viewsets.ModelViewSet, ReadWriteSerializerViewMixin):
    read_serializer = NoteReadSerializer
    write_serializer = NoteWriteSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsOTPVerified]
    filterset_class = NoteFilterSet
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ["title", "content"]

    def get_queryset(self):
        return Note.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"))
