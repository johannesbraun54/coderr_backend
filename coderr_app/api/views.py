from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from coderr_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import AllowAny


class ImageUploadView(APIView):
    pass


class ProfileView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
