import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models

from Djote import settings


class AuthUser(AbstractUser):
    class Meta:
        app_label = 'user'
