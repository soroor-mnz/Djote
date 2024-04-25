from django.db import models
from Djote.utils.model_utils import TimeStampMixin
from user.models import AuthUser


class Note(TimeStampMixin):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']