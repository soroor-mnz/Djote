import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from Djote.utils.view_utils import now
from main.models import Note
from main.tests.factories import NoteFactory
from user.tests.factories import UserFactory
from django.urls import reverse
from rest_framework import status


class NoteTestCase(TestCase):
    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

        self.note_1 = NoteFactory(user=self.user_1, title='blue', content="note number 1",
                                  created_at=now() - datetime.timedelta(days=7))
        self.note_2 = NoteFactory(user=self.user_1, title='red', content="note number 2")
        self.note_3 = NoteFactory(user=self.user_2, title='car', content="note number 3")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_note_creation(self):
        self.assertEqual(self.note_1.title, 'blue')
        self.assertEqual(self.note_1.content, 'note number 1')
        self.assertEqual(self.note_1.user, self.user_1)

    def test_note_str(self):
        self.assertEqual(str(self.note_1), 'blue')

    def test_list_api(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), Note.objects.all().count())

    def test_list_api_filter_user(self):
        response = self.client.get(reverse("note-list") + "?user=" + self.user_1.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), Note.objects.filter(user_id=self.user_1.id).count())

    def test_list_api_filter_title(self):
        response = self.client.get(reverse("note-list") + "?title=e")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), Note.objects.filter(title__icontains="e").count())

    def test_list_api_filter_content(self):
        response = self.client.get(reverse("note-list") + "?content=number")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), Note.objects.filter(content__icontains="number").count())

    def test_list_filter_date(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=2)
        end_date = datetime.datetime.now()
        response = self.client.get(
            reverse("note-list") + "?created_at_before=" + str(end_date) + "&created_at_after=" + str(start_date))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"),
                         Note.objects.filter(created_at__range=(start_date, end_date)).count())

    def test_retrieve_api(self):
        response = self.client.get(reverse('note-detail', kwargs={"pk": self.note_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], Note.objects.get(id=self.note_1.id).title)

    def test_create_api(self):
        data = {
            "title": "new note",
            "content": "this is a new content for new note.",
        }
        response = self.client.post(reverse("note-list"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertIsNotNone(Note.objects.filter(title=data["title"]).exists())

    def test_update_api(self):
        data = {
            "title": "new title"
        }
        response = self.client.patch(reverse('note-detail', kwargs={"pk": self.note_1.id}), data=data,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])
        self.assertIsNotNone(Note.objects.filter(title=data["title"]).exists())

    def test_update_api_invalid_user(self):
        data = {
            "title": "new title"
        }
        response = self.client.patch(reverse('note-detail', kwargs={"pk": self.note_3.id}), data=data,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
