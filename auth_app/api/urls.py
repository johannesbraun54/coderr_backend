from django.urls import path
from .views import RegistrationView, CustomLoginView, ImageUploadView, ProfileView, ProfileBusinessListView, ProfileCustomerListView, BaseInfoView

urlpatterns = [
     path('registration/', RegistrationView.as_view(), name='registration'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('uploads/', ImageUploadView.as_view(), name='image-upload'),
     path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail'),
     path('profiles/business/', ProfileBusinessListView.as_view(), name='profile-business-list'),
     path('profiles/customer/', ProfileCustomerListView.as_view(), name='profile-customer-list'),
     path('base-info/', BaseInfoView.as_view(), name="base-info")

]
