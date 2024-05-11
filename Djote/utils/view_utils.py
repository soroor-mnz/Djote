from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.permissions import BasePermission
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


class IsOTPVerified(BasePermission):
    """
    Custom permission class to check if the user is OTP verified.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Check if the user has an OTP device
                device = TOTPDevice.objects.get(user=request.user)
            except TOTPDevice.DoesNotExist:
                # If the user does not have an OTP device, return False
                return False

            # Check if the user has verified OTP
            return device.confirmed

        # If the user is not authenticated, return False
        return False


def now():
    return timezone.now()
