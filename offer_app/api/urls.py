from django.urls import path, include
from rest_framework import routers
from .views import OffersViewSet, OfferImageUploadView, OfferDetailView


router = routers.SimpleRouter()
router.register(r'offers', OffersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('uploads/', OfferImageUploadView.as_view(), name='image-upload'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetails-detail')
]
