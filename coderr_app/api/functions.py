from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status


def set_offer_min_delivery_time(request):
    details = request.data['details']
    delivery_times = []
    for detail in details:
        delivery_times.append(detail['delivery_time_in_days'])
    min_delivery_time = min(delivery_times)
    return min_delivery_time

def set_offer_min_price(request):
    details = request.data['details']
    prices = []
    for detail in details:
        price = float(detail['price'])
        prices.append(price)
        min_price = min(prices)
    return min_price


def patch_details(request, pk):
    validated_details = []
    old_offer_details = OfferDetails.objects.filter(offer_id=pk)
    new_offer_details = request.data['details']
    for i in range(len(new_offer_details)):
        new_detail = new_offer_details[i]
        current_detail_offer_type = new_detail['offer_type']
        current_patch_detail = old_offer_details.get(
            offer_type=current_detail_offer_type)
        detail_serializer = OfferDetailsSerializer(
            current_patch_detail, data=new_detail, partial=True, context={'request': request})
        if detail_serializer.is_valid():
            detail_serializer.save()
            validated_details.append(detail_serializer.data)
        else:
            return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return request


def get_offer_details(pk, request):
    validated_details = []
    details = OfferDetails.objects.filter(offer_id=pk)
    print(details)
    for detail in details:
        serializer = OfferDetailsSerializer(
            detail, context={'request': request})
        validated_details.append(serializer.data)
    return validated_details


def create_new_order(request):
    try:
        offer_detail_id = request.data['offer_detail_id']
        new_order = OfferDetails.objects.get(id=offer_detail_id)
        offer = Offer.objects.get(pk=new_order.offer_id)
        new_order = OfferDetails.objects.get(id=offer_detail_id)
        request.data['customer_user'] = request.user.id
        request.data['business_user'] = new_order.offer.user.id
        request.data['title'] = offer.title
        request.data['revisions'] = new_order.revisions
        request.data['delivery_time_in_days'] = new_order.delivery_time_in_days
        request.data['price'] = new_order.price
        request.data['features'] = new_order.features
        request.data['offer_type'] = new_order.offer_type
        request.data['status'] = "in_progress"
        return request
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
