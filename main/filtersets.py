from django_filters import FilterSet, CharFilter, DateTimeFromToRangeFilter

from main.models import Note


class NoteFilterSet(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    content = CharFilter(field_name="content", lookup_expr="icontains")
    user = CharFilter(field_name="user__username")
    created_at = DateTimeFromToRangeFilter(field_name="created_at")
    updated_at = DateTimeFromToRangeFilter(field_name="updated_at")

    class Meta:
        model: Note
        fields = ["user", "title", "content", "created_at", "updated_at"]
