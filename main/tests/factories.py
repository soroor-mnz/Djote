from factory.django import DjangoModelFactory
import factory
from main.models import Note


class NoteFactory(DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker("title")
    content = factory.Faker("content")
