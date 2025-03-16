from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from coderr_app.models import UserProfile, Offer, OfferDetails
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OfferImageUploadView(APIView):

#     def post(self, request, format=None):
#         print("request.data", request.data)
#         serializer = OfferImageUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def validate_offer_details(details, saved_offer_id):
    for detail in details:
        detail['offer_id'] = saved_offer_id
        details_serializer = OfferDetailsSerializer(data=detail)
        if details_serializer.is_valid():
            details_serializer.save()
            return Response(details_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OffersView(GenericAPIView):

    
    def get(self, request):
        serializer = OffersSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        # data['details'][0]['offer_id'] =
        # print("titles",data['details'][0]['title'])
        # print(data)
        details = request.data['details']
        serializer = OffersSerializer(data=request.data)
        if serializer.is_valid():
            saved_offer = serializer.save()
            validate_offer_details(details, saved_offer.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
