from django.urls import path, include
from .views import ImageUploadView, ProfileView, ProfileBusinessListView, ProfileCustomerListView, OfferDetailView, OfferImageUploadView, ReviewsListView, ReviewsDetailView, OrdersView, OrdersDetailView, OrderInProgressCountView, OrderCompleteCountView, BaseInfoView, OffersViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'offers', OffersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('uploads/', ImageUploadView.as_view(), name='image-upload'),
    path('uploads/', OfferImageUploadView.as_view(), name='image-upload'),
    path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfileBusinessListView.as_view(), name='profile-business-list'),
    path('profiles/customer/', ProfileCustomerListView.as_view(), name='profile-customer-list'),
    # path('offers/', OffersView.as_view(), name='offers-list'),
    # path('offers/<int:pk>/', SingleOfferView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetails-detail'),
    path('reviews/', ReviewsListView.as_view(), name="reviews-list"),
    path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name='reviews-detail'),
    path('orders/', OrdersView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders-detail'),
    path('order-count/<int:pk>/', OrderInProgressCountView.as_view(), name="orders-count"),
    path('completed-order-count/<int:pk>/', OrderCompleteCountView.as_view(), name="orders-complete-count"),
    path('base-info/', BaseInfoView.as_view(), name="base-info")
]

