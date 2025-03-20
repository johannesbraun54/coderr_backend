from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Offer, OfferDetails
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.api.serializers import OffersSerializer


class TestOffers(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@mail.com')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.offer = Offer.objects.create(
            user_id=self.user.id,
            title="Grafikdesign-Paket",
            image="",  # Falls das Bild optional ist
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen."
        )

        # self.offerdetails = OfferDetails.objects.create(
        #     offer_id = self.offer.id,
        #     title="Basic Design",
        #     revisions=2,
        #     delivery_time_in_days=5,
        #     price=100,
        #     features=["Logo Design", "Visitenkarte"],
        #     offer_type="basic"
        # )

        # self.offerdetails = OfferDetails.objects.create(
        #     offer_id = self.offer.id,
        #     title="Standard Design",
        #     revisions=5,
        #     delivery_time_in_days=7,
        #     price=200,
        #     features=["Logo Design", "Visitenkarte", "Briefpapier"],
        #     offer_type="standard"
        # )

        # self.offerdetails = OfferDetails.objects.create(
        #     offer_id = self.offer.id,
        #     title="Premium Design",
        #     revisions=10,
        #     delivery_time_in_days=10,
        #     price=500,
        #     features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
        #     offer_type="premium"
        # )

        # self.offer.save()
        # self.offerdetails.save()

    def test_offer_post(self):
        url = reverse('offers-list')
        data = {
            "title": "Grafikdesign-Paket",
            "image": "",
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

    
    def test_patch_offer(self):
        url = reverse('offers-detail', kwargs={'pk':self.offer.id})
        patch_data = {'title':'UpdatePatchTest'}
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_offer(self):
        url = reverse('offers-list')
        response = self.client.get(url)
        # expected_data = OffersSerializer(instance=self.offer,context={'request': self.client})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertJSONEqual(response.content, expected_data)
        print("response.data", response.content)
