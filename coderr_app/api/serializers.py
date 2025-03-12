from rest_framework import serializers
from coderr_app.models import UserProfile, Offer, OfferDetails

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
    class Meta:
        model = OfferDetails
        fields = '__all__'
    
    offer_id = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), write_only=True)
        
class OffersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = '__all__'
    print("HIIIIIIII")        
    image = OfferImageUploadSerializer()
    details = OfferDetailsSerializer(many=True)
        
