from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path('uploads/', ImageUploadView.as_view(), name='image-upload')
]

