from rest_framework import serializers
from auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserprofileTypeSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)

class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','repeated_password']
        extra_kwargs = {

            'password': {
                'write_only': True
            }
    }

    def save(self):
        pw = self.validated_data.get('password')
        repeated_pw = self.validated_data.get('repeated_password')
        passwords_dont_match = bool(pw != repeated_pw)
        email_already_exists = User.objects.filter(
            email=self.validated_data.get('email')).exists()

        if passwords_dont_match:
            raise serializers.ValidationError(
                {"password": ["Das Passwort ist nicht gleich mit dem wiederholten Passwort"]
            })
        elif email_already_exists:
            raise serializers.ValidationError({
                "email": ["Diese E-Mail-Adresse wird bereits verwendet."]
            })
        account = User(username=self.validated_data['username'],
                              email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account

        
