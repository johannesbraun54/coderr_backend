from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import LargeResultsSetPagination
from .functions import validate_offer_details, get_detail_keyfacts


################################################ IMAGEUPLOAD_VIEWS ################################################

class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = OfferImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
################################################ PROFILE_VIEWS ################################################


class ProfileView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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

################################################ OFFER_VIEWS ################################################

class OffersView(GenericAPIView, ListModelMixin):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [AllowAny]
    filterset_fields = ['user', 'min_price', 'max_delivery_time']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request):
        request.data['user'] = request.user.id
        get_detail_keyfacts(request)
        details = request.data['details']
        serializer = OffersSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            saved_offer = serializer.save()
            validate_offer_details(details, saved_offer.id, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SingleOfferView(GenericAPIView, UpdateModelMixin, RetrieveModelMixin):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class OfferDetailView(GenericAPIView, RetrieveModelMixin, CreateModelMixin):

    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)






