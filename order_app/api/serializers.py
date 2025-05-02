from rest_framework import serializers
from order_app.models import Order
from offer_app.models import OfferDetails
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):

    offer_detail= serializers.PrimaryKeyRelatedField(queryset=OfferDetails.objects.all(),write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail']

    def validate(self, attrs):
        request = self.context.get('request', None)
        if request != None and request.method == 'PATCH':
            status = getattr(request.data, 'status', None)
            if len(attrs) != 1 and status == None:
                raise serializers.ValidationError("You can only update field 'status'")
        return super().validate(attrs)

class OrderCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['order_count']
    
    order_count = serializers.SerializerMethodField()
    
    def get_order_count(self, obj):
        return obj.received_orders.filter(status='in_progress').count()
    
class CompletedOrderCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['completed_order_count']
    
    completed_order_count = serializers.SerializerMethodField()
    
    def get_completed_order_count(self, obj):
        return obj.received_orders.filter(status='completed').count()