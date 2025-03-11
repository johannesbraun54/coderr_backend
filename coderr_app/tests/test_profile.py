from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import UserProfile
from django.urls import reverse
from django.contrib.auth.models import User



class TestProfile(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username='testuser',
                                        email='test@mail.com')
        UserProfile.objects.create(
                user= user.id,
                type= 'customer',
                username= 'testuser',
                email= 'test@mail.com'
        )
    
    def test_get_profile(self):
        url = reverse('profile-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        print("url", url)
        print(UserProfile.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        