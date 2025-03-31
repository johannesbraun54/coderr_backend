from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status


def validate_offer_details(details, saved_offer_id, request):
    for detail in details:
        detail['offer'] = saved_offer_id
        details_serializer = OfferDetailsSerializer(
            data=detail, context={'request': request})
        if details_serializer.is_valid():
            details_serializer.save()
        else:
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(details_serializer.data, status=status.HTTP_201_CREATED)


def get_detail_keyfacts(request):
    details = request.data['details']
    prices = []
    delivery_times = []
    for detail in details:
        prices.append(detail['price'])
        delivery_times.append(detail['delivery_time_in_days'])
        request.data['min_price'] = min(prices)
        request.data['max_delivery_time'] = max(delivery_times)

    return request


def create_new_order(request):
    offer_detail_id = request.data['offer_detail_id']
    print(offer_detail_id)
    new_order = OfferDetails.objects.all()[offer_detail_id]
    request.data['customer_user'] = request.user.id
    request.data['business_user'] = new_order.offer.user.id
    request.data['title'] = new_order.title
    request.data['revisions'] = new_order.revisions
    request.data['delivery_time_in_days'] = new_order.delivery_time_in_days
    request.data['price'] = new_order.price
    request.data['features'] = new_order.features
    request.data['offer_type'] = new_order.offer_type
    request.data['status'] = "in_progress"
    return request
