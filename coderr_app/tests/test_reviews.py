from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.api.serializers import OffersSerializer


class TestReviews(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@mail.com')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        UserProfile.objects.create(
            user=self.user,
            type='customer',
            username='testuser',
            email='test@mail.com'
        )

    def test_get_reviews(self):
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reviews(self):
        url = reverse('reviews-list')
        new_review = {
            "business_user": self.user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, new_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, new_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_reviews(self):
        url = reverse('reviews-detail')
        patch_review = {
            "description": "Nichts war toll!"
        }
        response = self.client.post(url, patch_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


