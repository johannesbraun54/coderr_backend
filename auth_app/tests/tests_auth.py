from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from rest_framework.authtoken.models import Token

class TestRegistration(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('registration')
        data = {"username": "testuser",
                "email": "test@example.com",
                "password": 'test',
                "repeated_password": 'test',
                "type": 'customer'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLogin(APITestCase):
    def setUp(self):
        self.client = APIClient()
        new_user = User.objects.create_user(username="testuser",
                                 email="test@example.com",
                                 password="test",
                                )
        UserProfile.objects.create(
            user=new_user,
            type='customer',
            username='testuser',
            email='test@mail.com'
        )

    def test_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'test'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestProfile(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='dertest'
                                             )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        UserProfile.objects.create(
            user=self.user,
            type='customer',
            username='testuser',
            email='test@mail.com'
        )

    def test_get_profile(self):
        url = reverse('profile-detail', kwargs={'user': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile(self):
        url = reverse('profile-detail', kwargs={'user': 1})
        data = {'email': 'test123@mail.com'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)