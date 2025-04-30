from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails, UserProfile, Review
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.api.serializers import OffersSerializer


class TestReviews(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(username="customeruser", email="customertest@mail.com")
        self.client = APIClient()
        self.token = Token.objects.create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.business_user = User.objects.create_user(username="businessuser", email="businessuser@mail.com")
        UserProfile.objects.create(
            user=self.customer_user,
            type='customer',
            username='customeruser',
            email='customertest@mail.com'
        )
        UserProfile.objects.create(
            user=self.business_user,
            type='business',
            username='businessuser',
            email='businessuser@mail.com'
        )

        
    def test_get_reviews(self):
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_reviews(self):
        url = reverse('reviews-list')
        new_review = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, new_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, new_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review(self):

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Alles war toll!")

        url = reverse('reviews-detail', kwargs={'pk': self.review.id})
        patch_review = {
            "description": "Nichts war toll!"
        }
        response = self.client.patch(url, patch_review, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Alles war toll!")
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
