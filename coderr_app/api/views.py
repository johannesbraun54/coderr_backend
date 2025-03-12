from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, ImageUploadSerializer, OffersSerializer
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


class ProfileBusinessListView(GenericAPIView, ListModelMixin):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProfileCustomerListView(GenericAPIView, ListModelMixin):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class OffersView(GenericAPIView):
    
    queryset = Offer.objects.all()
    serializer_class= OffersSerializer
    
    def post(self, request):
        pass