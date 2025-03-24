from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.api.serializers import OffersSerializer

class TestReviews(APITestCase):
     
    def test_get_reviews(self):
        url = reverse()