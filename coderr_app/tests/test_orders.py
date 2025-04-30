from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import Order, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from coderr_app.tests.test_functions import create_and_login_test_user, login_second_test_user, create_test_customer_userprofile, create_SECOND_test_user, create_test_order, create_test_offer, create_test_offerdetails


class TestOrders(APITestCase):
    def setUp(self):

        create_and_login_test_user(self)
        create_test_customer_userprofile(self)
        create_SECOND_test_user(self)
        self.second_userprofile = UserProfile.objects.create(
            user=self.second_user,
            type='business',
            username='businessuser',
            email='businessuser@mail.com'
        )
        create_test_offer(self)
        create_test_offerdetails(self)
        create_test_order(self)

    def test_get_orders(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_patch_order(self):
        login_second_test_user(self)
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        data = {"status": "completed"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_count_order(self):
        url = reverse('orders-count', kwargs={'pk': self.second_user.id})
        response = self.client.get(url)
        expected_order_count = {'order_count': 1}
        self.assertEqual(response.data, expected_order_count)

    def test_count_completed_order(self):
        url = reverse('orders-complete-count', kwargs={'pk': self.second_user.id})
        response = self.client.get(url)
        self.order.status = "completed"
        expected_order_count = {'completed_order_count': 0}
        self.assertEqual(response.data, expected_order_count)

    def test_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
