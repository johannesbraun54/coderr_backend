from rest_framework import serializers
from django.contrib.auth.models import User


def check_email_existence(mail_adress):
    if User.objects.filter(email=mail_adress).exists():
        raise serializers.ValidationError({
            "email": ["Diese E-Mail-Adresse wird bereits verwendet."]
        })


def check_password_match(pw, repeated_pw):
    if pw != repeated_pw:
        raise serializers.ValidationError({
            "password": ["Die Passwörter stimmen nicht überein."]
        })


def check_username_existence(new_username):
    if User.objects.filter(username=new_username).exists():
        raise serializers.ValidationError({
            "username": ["Dieser Username wird bereits verwendet."]
        })


class UserprofileTypeSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {

            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data.get('password')
        repeated_pw = self.validated_data.get('repeated_password')

        check_password_match(pw, repeated_pw)
        # check_username_existence(self.validated_data.get('username'))
        check_email_existence(self.validated_data.get('email'))

        account = User(username=self.validated_data['username'],
                       email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account
