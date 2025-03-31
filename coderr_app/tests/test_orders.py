from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails, UserProfile, Review
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestOrders(APITestCase):
    def setUp(self):
         pass
    
    def test_get_orders(self):
         url = reverse('order-list')