from django.urls import path
from .views import ImageUploadView, ProfileView

urlpatterns = [
    path('uploads/', ImageUploadView.as_view(), name='image-upload'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail')
]

