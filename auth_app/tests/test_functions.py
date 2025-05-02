from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from auth_app.models import UserProfile

def create_and_login_test_user(self):
    self.user = User.objects.create_user(
        username='testuser', email='test@mail.com', is_staff=True) 
    self.token = Token.objects.create(user=self.user)
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

def create_test_customer_userprofile(self):
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        type='customer',
        username='testuser',
        email='test@mail.com'
    )

def create_SECOND_test_user(self):
    self.second_user = User.objects.create_user(
        username='second_testuser', email='second_test@mail.com')
    
def login_second_test_user(self):
    self.token = Token.objects.create(user=self.second_user)
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


def create_test_business_userprofile(self):
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        type='business',
        username='testuser',
        email='test@mail.com'
    )