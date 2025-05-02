from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    TYPE_CHOICES = [('customer', 'customer'), ('business', 'business')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    first_name = models.CharField(max_length=64, null=True, default="add information")
    last_name = models.CharField(max_length=64, null=True, default="add information")
    file = models.ImageField(upload_to='uploads/',null=True, default="add information")
    location = models.CharField(max_length=64, null=True, default="add information")
    tel = models.CharField(max_length=64, null=True, default="add information")
    description = models.CharField(max_length=256, null=True, default="add information")
    working_hours = models.CharField(max_length=24, null=True, default="add information")
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Review(models.Model):
    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    business_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)