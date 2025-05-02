from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    TYPE_CHOICES = [('customer', 'customer'), ('business', 'business')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    username = models.CharField(max_length=64)
    email = models.EmailField()
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    file = models.ImageField(upload_to='uploads/',null=True)
    location = models.CharField(max_length=64, null=True, default="add information")
    tel = models.CharField(max_length=64, null=True, default="add information")
    description = models.CharField(max_length=256, null=True, default="add information")
    working_hours = models.CharField(max_length=24, null=True, default="add information")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
