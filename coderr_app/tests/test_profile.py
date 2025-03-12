from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import UserProfile
from django.urls import reverse
from django.contrib.auth.models import User


class TestProfile(APITestCase):

    def setUp(self):
        self.client = APIClient()
        new_user = User.objects.create_user(username='testuser',
                                        email='test@mail.com')
        UserProfile.objects.create(
            user=new_user,
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

