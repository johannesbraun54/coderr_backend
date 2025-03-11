from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    file = models.ImageField(upload_to='uploads/', null=True)
    location = models.CharField(max_length=64, null=True)
    tel = models.IntegerField(null=True)
    description = models.CharField(max_length=256, null=True)
    working_hours = models.CharField(max_length=24, null=True)
    created_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/', null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_delivery_time = models.IntegerField()
    # user_details = append in view


class OfferDetails(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='offer_details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
