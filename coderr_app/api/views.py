from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from coderr_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import AllowAny



class ImageUploadView(APIView):
    pass

class ProfileView(GenericAPIView, RetrieveModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)