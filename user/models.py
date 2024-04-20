import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models

from Djote import settings
from Djote.utils.model_utils import SoftDeleteMixin, TimeStampMixin


class AuthUser(AbstractUser, SoftDeleteMixin, TimeStampMixin):
    class Meta:
        app_label = 'user'
        ordering = ['created_at']
