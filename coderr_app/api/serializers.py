from rest_framework import serializers
from coderr_app.models import UserProfile, Review, Order
from offer_app.models import OfferDetails
from django.contrib.auth.models import User

class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['file']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']

    def _valdiate_double_rate(self, request):
        has_already_rated_user = Review.objects.filter(
            business_user=self.initial_data.get('business_user'), reviewer=request.user).exists()
        if has_already_rated_user:
            raise serializers.ValidationError(
                {'error': 'already rated this user'})

    def _validate_user_type(self):
        business_user = User.objects.get(pk=self.initial_data.get('business_user'))
        if business_user.userprofile.type == "customer":
            raise serializers.ValidationError(
                {'error': 'you can only rate business users'})

    def _validate_patch_fields(self, request):
        if request.method == 'PATCH':
            request_contains_reviewer = request.data.get('reviewer', None)
            request_contains_business_user = request.data.get('business_user', None)
            if request_contains_reviewer or request_contains_business_user:
                raise serializers.ValidationError(
                    {'error': 'you can only patch rating and description'})

    def validate_business_user(self, value):
        request = self.context.get('request')
        self._valdiate_double_rate(request)
        self._validate_user_type()
        self._validate_patch_fields(request)
        return value

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review


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