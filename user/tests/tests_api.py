import datetime
from django.test import TestCase

from Djote.utils.view_utils import now
from user.api.serializers.serializers import UserReadSerializer
from user.models import AuthUser
from user.tests.factories import UserFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.user_1 = UserFactory(date_joined=now() - datetime.timedelta(days=7))
        self.user_2 = UserFactory()
        self.user_3 = UserFactory()
        self.user_4 = UserFactory(is_deleted=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_list_api(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.all().count())
        self.assertEqual(response.data.get("results")[0]["username"],
                         AuthUser.objects.all().order_by('created_at').first().username)
        user_serializer = UserReadSerializer
        for field in user_serializer.Meta.fields:
            self.assertIn(field, response.data.get("results")[0])

    def test_list_api_filter_first_name(self):
        response = self.client.get(reverse("user-list") + "?first_name=" + self.user_1.first_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.filter(first_name=self.user_1.first_name).count())
        self.assertEqual(response.data.get("results")[0]["first_name"],
                         AuthUser.objects.get(first_name=self.user_1.first_name).first_name)

    def test_list_api_filter_last_name(self):
        response = self.client.get(reverse("user-list") + "?last_name=" + self.user_3.last_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.filter(last_name=self.user_3.last_name).count())
        self.assertEqual(response.data.get("results")[0]["last_name"],
                         AuthUser.objects.get(last_name=self.user_3.last_name).last_name)

    def test_list_api_filter_email(self):
        response = self.client.get(reverse("user-list") + "?email=" + self.user_3.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.filter(email=self.user_3.email).count())
        self.assertEqual(response.data.get("results")[0]["email"], AuthUser.objects.get(email=self.user_3.email).email)

    def test_list_api_filter_is_active(self):
        response = self.client.get(reverse("user-list") + "?is_active=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.filter(is_active=True).count())

    def test_list_api_filter_date_joined(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=2)
        end_date = datetime.datetime.now()
        response = self.client.get(
            reverse("user-list") + "?date_joined_before=" + str(end_date) + "&date_joined_after=" + str(start_date))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"),
                         AuthUser.objects.filter(date_joined__range=(start_date, end_date)).count())

    def test_list_api_filter_is_deleted(self):
        response = self.client.get(reverse("user-list") + "?is_deleted=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), AuthUser.objects.filter(is_deleted=True).count())

    def test_retrieve_api(self):
        response = self.client.get(reverse('user-detail', kwargs={"username": self.user_1.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"],
                         AuthUser.objects.get(username=self.user_1.username).first_name)

    def test_create_api(self):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@email.ex",
            "username": "user_name",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertIsNotNone(AuthUser.objects.filter(username=data["username"]).exists())

    def test_create_api_invalid_email(self):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "invalid_email",
            "username": "user_name",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_api(self):
        data = {
            "first_name": "new name"
        }
        response = self.client.patch(reverse('user-detail', kwargs={"username": self.user_1.username}), data=data,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data.get("first_name"))
        self.assertIsNotNone(AuthUser.objects.filter(first_name=data.get("first_name")).exists())

    def test_soft_delete_api(self):
        response = self.client.delete(reverse('user-detail', kwargs={"username": self.user_1.username}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(AuthUser.objects.filter(username=self.user_1.username).exists())
        self.assertTrue(AuthUser.objects.filter(username=self.user_1.username).first().is_deleted)

    def test_restore_user(self):
        response = self.client.delete(reverse('user-detail', kwargs={"username": self.user_1.username}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deleted_user = AuthUser.objects.get(username=self.user_1.username)
        deleted_user.restore()
        self.assertFalse(AuthUser.objects.filter(username=self.user_1.username).first().is_deleted)
