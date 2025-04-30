from coderr_app.models import Offer, OfferDetails, Review
from rest_framework.response import Response
from rest_framework import status


def set_offer_min_delivery_time(request):
    details = request.data.get('details', None)
    delivery_times = []
    for detail in details:
        delivery_times.append(detail['delivery_time_in_days'])
    min_delivery_time = min(delivery_times)
    return min_delivery_time

def set_offer_min_price(details):
    prices = []
    for detail in details:
        if isinstance(detail, dict):
            price = float(detail['price'])
        else:
            price = float(detail.price)
        prices.append(price)
        min_price = min(prices)
    return float(min_price) 

def set_user_details(user):
    user_details = {'first_name': user.userprofile.first_name, 'last_name': user.userprofile.last_name , 'username': user.username }
    return user_details

def get_rating_average(reviews_count):
    ratings = []
    reviews = Review.objects.all()
    rating_sum = 0
    for i in range(reviews_count):
        review = reviews[i]
        rating = review.rating
        ratings.append(rating)
    for rating in ratings:
        rating_sum += rating
        review_rating_average = round(rating_sum / len(ratings), 1)
    return review_rating_average




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

    

