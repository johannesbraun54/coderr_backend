from rest_framework import serializers
from coderr_app.models import UserProfile

class ImageUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['file']

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        
