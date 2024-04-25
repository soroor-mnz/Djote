from factory.django import DjangoModelFactory
import factory
from user.models import AuthUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
