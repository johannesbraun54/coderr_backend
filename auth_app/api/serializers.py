from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from .serializer_helpers import check_password_match



class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates email uniqueness and password matching.
    """
    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {

            'password': {
                'write_only': True
            },

            'email': {
                'required': True
            }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exits.")
        return value

    def save(self):
        pw = self.validated_data.get('password')
        repeated_pw = self.validated_data.get('repeated_password')
        check_password_match(pw, repeated_pw)

        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account

class ImageUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading user profile images.
    """
    class Meta:
        model = UserProfile
        fields = ['file']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for complete user profiles.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']