from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails
from django.urls import reverse
from django.contrib.auth.models import User



# class TestOffers(APITestCase):
    
#     # def setUp(self):
#     #     pass
    
#     # def test_offer_post():
#     #     pass