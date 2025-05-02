from offer_app.models import Offer, OfferDetails

def create_new_order(request):
    order = {}
    offer_detail_id = request.data.get('offer_detail_id', None)
    offer_detail = OfferDetails.objects.get(id=offer_detail_id)
    offer = Offer.objects.get(pk=offer_detail.offer_id)
    order['offer_detail'] = offer_detail_id
    order['customer_user'] = request.user.id
    order['business_user'] = offer_detail.offer.user.id
    order['title'] = offer.title
    order['revisions'] = offer_detail.revisions
    order['delivery_time_in_days'] = offer_detail.delivery_time_in_days
    order['price'] = offer_detail.price
    order['features'] = offer_detail.features
    order['offer_type'] = offer_detail.offer_type
    order['status'] = "in_progress"
    return order