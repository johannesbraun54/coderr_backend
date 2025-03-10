from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import UserProfile

# Create your tests here.


class TestRegistration(APITestCase):
    def setUp(self): 
        self.client = APIClient()
    #     self.user = UserProfile.user.objects.create_user()

    def test_create_user(self):
        url = reverse('registration')
        data = {"username": "testuser",
                "email": "test@example.com",
                "password": 'test',
                "repeated_password": 'test',
                "type": 'customer'
                }
        print("data",data)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
