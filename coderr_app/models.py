from django.db import models
from django.contrib.auth.models import User




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
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='offer_details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    
    
# [
# {
# "id": 1,
# "user": 1,
# "title": "Website Design"
# ,
# "image": null,
# "description": "Professionelles Website-Design...
# "
# "created_at": "2024-09-25T10:00:00Z"
# ,
# "updated_at": "2024-09-28T12:00:00Z"
# ,
# "details": [
# {"id": 1,
# {"id": 2,
# {"id": 3,
# "url": "/offerdetails/1/"},
# "url": "/offerdetails/2/"},
# "url": "/offerdetails/3/"}
# ],
# "min_price": 100.00,
# "min_delivery_time": 7,
# "user_details": {
# "first_name": "John"
# ,
# "last_name": "Doe"
# ,
# "username": "jdoe"
# ,
# }
# }
# ]
