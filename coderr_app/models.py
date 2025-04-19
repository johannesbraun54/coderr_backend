from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    first_name = models.CharField(
        max_length=64, null=True, default="add information")
    last_name = models.CharField(
        max_length=64, null=True, default="add information")
    file = models.ImageField(upload_to='uploads/',
                             null=True, default="add information")
    location = models.CharField(
        max_length=64, null=True, default="add information")
    tel = models.CharField(max_length=64, null=True, default="add information")
    description = models.CharField(
        max_length=256, null=True, default="add information")
    working_hours = models.CharField(
        max_length=24, null=True, default="add information")
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/', null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_delivery_time = models.IntegerField()


class OfferDetails(models.Model):

    TYPE_CHOICES = [('basic', 'Basic'),
                    ('standard', 'Standard'),
                    ('premium', 'Premium')]

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255, choices=TYPE_CHOICES)


class Review(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    business_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_user')
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_user')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
