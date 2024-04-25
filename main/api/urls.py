from django.urls import path

from main.api.views.views import NoteViewSet

urlpatterns = [
    path('notes/', NoteViewSet.as_view({'get': "list", "post": "create"}), name='note-list'),
    path('notes/<int:pk>/', NoteViewSet.as_view({'get': "retrieve", "patch": "partial_update", "delete": "destroy"}),
         name='note-detail'),
]