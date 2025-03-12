from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from coderr_app.models import UserProfile
from .serializers import UserProfileSerializer, ImageUploadSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class ImageUploadView(APIView):
    
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ProfileView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user'
            
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
