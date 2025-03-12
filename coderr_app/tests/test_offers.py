from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails
from django.urls import reverse
from django.contrib.auth.models import User


class TestOffers(APITestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username='testuser',
                                        email='test@mail.com')

    def test_offer_post(self):
        url = reverse('offers-list')
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100.00,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500.00,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
