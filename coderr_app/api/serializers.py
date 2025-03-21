from rest_framework import serializers
from coderr_app.models import UserProfile, Offer, OfferDetails
from django.contrib.auth.models import User


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

    # details = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='offer-detail')
    details = OfferDetailsSerializer(many=True, read_only=True, fields=('id', 'url'))
