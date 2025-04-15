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

    offer = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.all())


class OffersSerializer(serializers.ModelSerializer):


    class Meta:
        model = Offer
        fields = '__all__'
        
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    
    details = OfferDetailsSerializer(
        many=True, read_only=True, fields=('id', 'url'))
    
    # details_ids = serializers.PrimaryKeyRelatedField(queryset=OfferDetails.objects.all(), many=True, write_only=True, source="details")



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

    
