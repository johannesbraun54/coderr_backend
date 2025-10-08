from rest_framework import serializers
from django.contrib.auth.models import User

def check_email_existence(mail_adress):
    """
    Checks if the provided email address already exists in the User model.
    Raises a ValidationError if the email already exists.
    """
    if User.objects.filter(email=mail_adress).exists():
        raise serializers.ValidationError({
            "email": ["Email already exits."]
        })

def check_password_match(pw, repeated_pw):
    """
    Validates that the provided password and repeated password match.
    Raises a ValidationError if they do not match.
    """
    if pw != repeated_pw:
        raise serializers.ValidationError({
            "password": ["Passwords don't matching."]
        })