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

def patch_details(details_data, details):
    for detail_data in details_data:
        offer_type = detail_data.get('offer_type', None)
        detail = details.get(offer_type=offer_type)
        detail.title = detail_data.get('title', detail.title)
        detail.revisions = detail_data.get('revisions', detail.revisions)
        detail.delivery_time_in_days = detail_data.get(
            'delivery_time_in_days', detail.delivery_time_in_days)
        detail.price = detail_data.get('price', detail.price)
        detail.features = detail_data.get('features', detail.features)
        detail.save()
