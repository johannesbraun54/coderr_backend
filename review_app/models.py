from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    business_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)