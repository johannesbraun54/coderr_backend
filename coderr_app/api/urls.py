from django.urls import path
from .views import ImageUploadView, ProfileView

urlpatterns = [
    path('uploads/', ImageUploadView.as_view(), name='image-upload'),
    path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail')
]

