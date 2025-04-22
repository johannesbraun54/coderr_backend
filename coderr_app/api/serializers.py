from rest_framework import serializers
from coderr_app.models import UserProfile, Offer, OfferDetails, Review, Order
from django.contrib.auth.models import User
from rest_framework import status
from .functions import set_offer_min_price, set_offer_min_delivery_time


class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['file']


class OfferImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['image']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class OfferDetailsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

    # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = OfferDetails
        fields = ['id', 'url', 'offer', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['offer']


class OffersSerializer(serializers.ModelSerializer):

    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'min_price', 'min_delivery_time', 'details']
        read_only_fields = ['min_price', 'min_delivery_time']
        write_only_fields = ['user']

    def _validate_details_length(self, details):
        if len(details) != 3:
            raise serializers.ValidationError(
                {'error': 'offer have to include exact 3 details'})

    def _get_current_offer_types(self, details):
        expected_types = {'basic', 'standard', 'premium'}
        received_types = {detail.get('offer_type')for detail in details}
        if received_types != expected_types:
            raise serializers.ValidationError(
                {'error': 'each offer must contain the following offertypes once : basic, standard, premium'})

    def validate_details(self, value):
        request = self.context.get('request')
        if request.method == 'POST':
            self._validate_details_length(value)
            self._get_current_offer_types(value)
        return value

    def create(self, validated_data):
        details = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details:
            OfferDetails.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        request = self.context.get("request")
        details_data = validated_data.pop('details')
        details = instance.details.all()

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)

        for detail_data in details_data:
            offer_type = detail_data['offer_type']
            detail = details.get(offer_type=offer_type)
            detail.title = detail_data.get('title', detail.title)
            detail.revisions = detail_data.get('revisions', detail.revisions)
            detail.delivery_time_in_days = detail_data.get(
                'delivery_time_in_days', detail.delivery_time_in_days)
            detail.price = detail_data.get('price', detail.price)
            detail.features = detail_data.get('features', detail.features)
            detail.save()

        instance.min_price = set_offer_min_price(instance.details.all())
        instance.min_delivery_time = set_offer_min_delivery_time(request)
        instance.save()

        return instance


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
        business_user = User.objects.get(
            pk=self.initial_data.get('business_user'))
        if business_user.userprofile.type == "customer":
            raise serializers.ValidationError(
                {'error': 'you can only rate business users'})

    def _validate_patch_fields(self, request):
        if request.method == 'PATCH':
            request_contains_reviewer = request.data.get('reviewer', None)
            request_contains_business_user = request.data.get(
                'business_user', None)
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
    offer_detail_id= serializers.PrimaryKeyRelatedField(queryset=OfferDetails.objects.all(), source='offer_detail',write_only=True)


    class Meta:
        model = Order
        exclude = ['offer_detail']
        read_only_fields = ['title', 'revisions', 'delivery_time_in_days',
                            'price', 'features', 'offer_type', 'status', 'customer_user', 'business_user']

    def validate(self, attrs):
        request = self.context.get('request')
        print("request.data",request.data)
        if request.method == 'POST':
            offer_detail_id = self.initial_data.get('offer_detail_id')
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
            order = {
                "offer_detail_id": offer_detail_id,
                "customer_user": request.user,
                "business_user": offer_detail.offer.user,
                "title": offer_detail.title,
                "revisions": offer_detail.revisions,
                "delivery_time_in_days": offer_detail.delivery_time_in_days,
                "price": offer_detail.price,
                "features": offer_detail.features,
                "offer_type": offer_detail.offer_type,
                "status": "in_progress"
            }
            attrs = order
        else:
           attrs =  request.data
        return super().validate(attrs)
