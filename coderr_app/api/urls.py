from django.urls import path
from .views import ImageUploadView, ProfileView, ProfileBusinessListView, ProfileCustomerListView, OffersView, OfferDetailView, SingleOfferView, OfferImageUploadView, ReviewsView

urlpatterns = [
    path('uploads/', ImageUploadView.as_view(), name='image-upload'),
    path('uploads/', OfferImageUploadView.as_view(), name='image-upload'),
    path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfileBusinessListView.as_view(), name='profile-business-list'),
    path('profiles/customer/', ProfileCustomerListView.as_view(), name='profile-customer-list'),
    path('offers/', OffersView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', SingleOfferView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetails-detail'),
    path("reviews/", ReviewsView.as_view(), name="reviews-list")
]

