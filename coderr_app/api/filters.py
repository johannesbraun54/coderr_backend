from coderr_app.models import Offer
from django_filters import rest_framework as filters



class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user')
    max_delivery_time = filters.NumberFilter(field_name="min_delivery_time", lookup_expr="lte") 
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr="gte")
    class Meta:
        model = Offer
        fields = []
        