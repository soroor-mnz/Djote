from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone


class ReadWriteSerializerViewMixin(GenericViewSet):
    """
    a mixin to separate read and write serializers
    """

    read_actions = ["retrieve", "list"]
    read_serializer = None
    write_serializer = None

    def get_serializer_class(self):
        if self.action in self.read_actions:
            return self.read_serializer
        else:
            return self.write_serializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 200


def now():
    return timezone.now()
