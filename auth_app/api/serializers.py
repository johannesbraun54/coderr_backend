from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import UserProfile

def check_email_existence(mail_adress):
    if User.objects.filter(email=mail_adress).exists():
        raise serializers.ValidationError({
            "email": ["Email already exits."]
        })

def check_password_match(pw, repeated_pw):
    if pw != repeated_pw:
        raise serializers.ValidationError({
            "password": ["Passwords don't matching."]
        })

class RegistrationSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = UserProfile
        fields = ['file']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']