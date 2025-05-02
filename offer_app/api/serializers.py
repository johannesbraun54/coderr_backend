from rest_framework import serializers
from offer_app.models import Offer, OfferDetails
from django.contrib.auth.models import User
from rest_framework import status
from .functions import set_offer_min_price, set_offer_min_delivery_time, patch_details

class OfferImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['image']

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
        fields = ['id', 'url', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['offer']

class OffersSerializer(serializers.ModelSerializer):

    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
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
        
    def _check_offer_types_at_patch(self, details):
        for detail in details:
            offer_type = detail.get('offer_type', None)
            if offer_type == None:
                raise serializers.ValidationError({'error': 'for patching the accordingly detail, field offer_type is required'})

    def validate_details(self, value):
        request = self.context.get('request')
        if request.method == 'POST':
            self._validate_details_length(value)
            self._get_current_offer_types(value)
        elif request.method == 'PATCH':
            self._check_offer_types_at_patch(value)
        return value

    def create(self, validated_data):
        details = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details:
            OfferDetails.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        request = self.context.get("request")
        details_data = validated_data.pop('details', None)
        details = instance.details.all()

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)

        if details_data != None:
            patch_details(details_data, details)            
            instance.min_price = set_offer_min_price(instance.details.all())
            instance.min_delivery_time = set_offer_min_delivery_time(request)
        instance.save()

        return instance
    
class OfferRetrieveSerializer(OffersSerializer):
    details = OfferDetailsSerializer(many=True, fields=('id', 'url'))

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time']
        
class OfferListSerializer(OfferRetrieveSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']