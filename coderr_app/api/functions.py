from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status


def validate_offer_details(details, saved_offer_id, request):
    validated_details = []
    for detail in details:
        detail['offer'] = saved_offer_id
        details_serializer = OfferDetailsSerializer(
            data=detail, context={'request': request})
        if details_serializer.is_valid():
            details_serializer.save()
            validated_details.append(details_serializer.data)
        else:
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return validated_details


def set_detail_keyfacts(request):
    details = request.data['details']
    prices = []
    delivery_times = []
    for detail in details:
        prices.append(float(detail['price']))
        delivery_times.append(detail['delivery_time_in_days'])

    request.data['min_price'] = str(min(prices))
    request.data['min_delivery_time'] = min(delivery_times)
    return request


def patch_details(request, pk):
    set_detail_keyfacts(request)
    old_offer_details = OfferDetails.objects.filter(offer_id=pk)
    for i in range(3):
        old_detail = old_offer_details[i]
        patched_detail = request.data['details'][i]
        detail_serializer = OfferDetailsSerializer(old_detail, data=patched_detail, partial=True)
        if detail_serializer.is_valid():
            detail_serializer.save()
        else:
            return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return request


def create_new_order(request):
    offer_detail_id = request.data['offer_detail_id']
    new_order = OfferDetails.objects.filter(id=offer_detail_id).exists()
    if new_order:
        new_order = OfferDetails.objects.get(id=offer_detail_id)
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
    else:
        return False
