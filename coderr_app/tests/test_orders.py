from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Order, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.tests.test_functions import create_and_login_test_user, create_test_business_userprofile, create_test_customer_userprofile, create_and_login_SECOND_test_user, create_test_order


class TestOrders(APITestCase):
    def setUp(self):

        create_and_login_test_user(self)
        create_test_customer_userprofile(self)
        create_and_login_SECOND_test_user(self)
        self.second_userprofile = UserProfile.objects.create(
            user=self.second_user,
            type='business',
            username='businessuser',
            email='businessuser@mail.com'
        )
        create_test_order(self)

    def test_get_orders(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_patch_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk':self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)