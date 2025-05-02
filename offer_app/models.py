from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/', null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    min_price = models.FloatField()
    min_delivery_time = models.IntegerField()
    user_details = models.JSONField()



class OfferDetails(models.Model):

    TYPE_CHOICES = [('basic', 'Basic'),
                    ('standard', 'Standard'),
                    ('premium', 'Premium')]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.FloatField()
    features = models.JSONField()
    offer_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
