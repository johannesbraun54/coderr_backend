from rest_framework import serializers
from coderr_app.models import UserProfile, Offer, OfferDetails, Review, Order
from django.contrib.auth.models import User
from rest_framework import status


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
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']

    # def validate_details(self, value):
    #     if len(value) == 3:
    #         return value
    #     else:
    #         raise serializers.ValidationError({'error' : 'offer includes less then 3 details'}) 

    def create(self, validated_data):
        details = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details:
            OfferDetails.objects.create(offer=offer, **detail)
        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        details = instance.details

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)

        for detail in details:
            detail = OfferDetails.objects.get(offer_id=instance.id, offer_type=detail['offer_type'])
            OfferDetails.objects.update(**detail)
        return instance


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = []

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        new_business_user = validated_data.get('business_user')
        new_reviewer = validated_data.get('reviewer')
        has_already_rated_user = Review.objects.filter(
            business_user=new_business_user, reviewer=new_reviewer).exists()
        if not has_already_rated_user:
            return super().create(validated_data)
        else:
            raise serializers.ValidationError(
                'du hast den user schonmal bewertet', status.HTTP_400_BAD_REQUEST)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
