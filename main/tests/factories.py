from factory.django import DjangoModelFactory
import factory
from main.models import Note
from user.tests.factories import UserFactory


class NoteFactory(DjangoModelFactory):
    class Meta:
        model = Note

    user = UserFactory()
    title = factory.Faker("title")
    content = factory.Faker("content")
