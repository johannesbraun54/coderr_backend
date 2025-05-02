from django.db import models
from django.contrib.auth.models import User
from offer_app.models import OfferDetails

class Order(models.Model):

    STATUS_CHOICES = [('in_progress', 'in_progress'),('completed', 'completed'), ('cancelled', 'cancelled')]
    offer_detail = models.ForeignKey(OfferDetails, related_name='offer_detail', on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)