from django_filters import CharFilter, BooleanFilter, DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet

from user.models import AuthUser


class UserFilterSet(FilterSet):
    first_name = CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = CharFilter(field_name="last_name", lookup_expr="icontains")
    email = CharFilter(field_name="email", lookup_expr="icontains")
    is_active = BooleanFilter(field_name="is_active")
    date_joined = DateTimeFromToRangeFilter(field_name="date_joined")
    is_deleted = BooleanFilter(field_name="is_deleted")

    class Meta:
        model: AuthUser
        fields = ["first_name", "last_name", "email", "is_active", "date_joined", "is_deleted"]
