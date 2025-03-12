from django.urls import path
from .views import ImageUploadView, ProfileView, ProfileBusinessListView, ProfileCustomerListView

urlpatterns = [
    path('uploads/', ImageUploadView.as_view(), name='image-upload'),
    path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfileBusinessListView.as_view(), name='profile-business-list'),
    path('profiles/customer/', ProfileCustomerListView.as_view(), name='profile-customer-list')
]

