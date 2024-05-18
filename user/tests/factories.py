from factory.django import DjangoModelFactory
from user.models import AuthUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser
