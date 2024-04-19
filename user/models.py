import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models

from Djote import settings
from Djote.utils.model_utils import SoftDeleteMixin


class AuthUser(AbstractUser, SoftDeleteMixin):
    class Meta:
        app_label = 'user'
