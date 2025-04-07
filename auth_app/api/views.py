from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserprofileTypeSerializer
from rest_framework.response import Response
from coderr_app.models import UserProfile
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from coderr_app.api.serializers import UserProfileSerializer


def set_user_profile(profile_data):
    serializer = UserProfileSerializer(data=profile_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("profile_serializer.errors",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        p_type = request.data.pop('type')
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            set_user_profile({'user': saved_account.id, 'type': p_type, 'username': saved_account.username,'email': saved_account.email})
            data = {
                'token': token.key,
                'username': saved_account.username,
                'user_id': saved_account.id,
                'is_superuser': True
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
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
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
