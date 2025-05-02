from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from auth_app.tests.test_functions import create_and_login_test_user , create_test_business_userprofile
from offer_app.tests.test_functions import create_test_offer, create_test_offerdetails


class TestOffers(APITestCase):

    def setUp(self):
        create_and_login_test_user(self)
        create_test_business_userprofile(self)
        create_test_offer(self)
        create_test_offerdetails(self)
        
    def test_offer_post(self):
        url = reverse('offer-list')
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_offer(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offerdetail_detail(self):
        url = reverse('offerdetails-detail',
                      kwargs={'pk': self.offerdetails.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        patch_data = {'title': 'UpdatePatchTest'}
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_offer(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_offer_detail(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
