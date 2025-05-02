from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserProfileSerializer, ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status, generics
from auth_app.models import UserProfile
from offer_app.models import Offer
from review_app.models import Review
from .functions import set_user_profile, get_rating_average
from .permissions import IsOwnerPermission


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        p_type = request.data.pop('type', None)
        if p_type in ['customer','business']:
            serializer = RegistrationSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                saved_account = serializer.save()
                set_user_profile({'user': saved_account.id, 'type': p_type, 'username': saved_account.username, 'email': saved_account.email})
                token, created = Token.objects.get_or_create(user=saved_account)
                data = {
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email,
                    'user_id': saved_account.id
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {'error': 'field type is required and should be included in UserProfile.TYPE_CHOICES'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerPermission]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'

class ProfileBusinessListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserProfileSerializer

class ProfileCustomerListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserProfileSerializer

class BaseInfoView(GenericAPIView):

    permission_classes = [AllowAny]

    def get(self, request):
        offer_count = len(Offer.objects.all())
        business_profile_count = len(
            UserProfile.objects.filter(type="business"))
        reviews_count = len(Review.objects.all())
        base_info_data = {
            "review_count": reviews_count,
            "average_rating": get_rating_average(reviews_count),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }
        return Response(base_info_data)

