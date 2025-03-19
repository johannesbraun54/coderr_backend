from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("serializer.data",serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("serializer.errors",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferImageUploadView(APIView):

    def post(self, request, format=None):
        print("request.data", request.data)
        serializer = OfferImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("serializer.errors",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class OfferDetailView(GenericAPIView):
    def get(self, request):
        serializer = OfferDetailsSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def post(self, request):
        serializer = OfferDetailsSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def validate_offer_details(details, saved_offer_id):
    for detail in details:
        print("detail", detail)
        detail['offer'] = saved_offer_id
        details_serializer = OfferDetailsSerializer(data=detail)
        if details_serializer.is_valid():
            details_serializer.save()
        else:
            print("Serializer Errors:", details_serializer.errors)
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(details_serializer.data, status=status.HTTP_201_CREATED)


class SingleOfferView(GenericAPIView, UpdateModelMixin):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    

class OffersView(GenericAPIView):

    # def get(self, request):
    #     offers = Offer.objects.all()
    #     serializer = OffersSerializer(offers, many=True, context={'request':request})
    #     return Response(serializer.data)
         
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        details = request.data['details']
        serializer = OffersSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            saved_offer = serializer.save()
            validate_offer_details(details, saved_offer.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
