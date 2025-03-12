from rest_framework import serializers
from coderr_app.models import UserProfile, Offer, OfferDetails

class ImageUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['file']

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        fields = '__all__'
        
class OffersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = ['title', 'description']
        details = OfferDetailsSerializer()
        
