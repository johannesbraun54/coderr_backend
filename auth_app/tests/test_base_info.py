from django.urls import reverse
from rest_framework.test import APITestCase
from auth_app.tests.test_functions import create_and_login_test_user, create_SECOND_test_user, create_test_customer_userprofile
from offer_app.tests.test_functions import create_test_offer, create_test_offerdetails
from auth_app.models import UserProfile
from review_app.tests.test_functions import create_test_review


class TestBaseInfo(APITestCase):

    def setUp(self):
        create_and_login_test_user(self)
        create_test_customer_userprofile(self)
        create_SECOND_test_user(self)
        self.userprofile = UserProfile.objects.create(
            user=self.second_user,
            type='business',
            username='testuser',
            email='test@mail.com'
        )

        create_test_offer(self)
        create_test_offerdetails(self)
        create_test_review(self)

    def test_get_base_info(self):

        url = reverse('base-info')
        expected_data = {
            "review_count": 1,
            "average_rating": 4.0,
            "business_profile_count": 1,
            "offer_count": 1
        }
        response = self.client.get(url)
        self.assertEqual(response.data, expected_data)
