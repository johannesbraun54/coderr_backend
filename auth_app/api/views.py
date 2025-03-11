from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserprofileTypeSerializer
from rest_framework.response import Response
from coderr_app.models import UserProfile
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from coderr_app.api.serializers import UserProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        p_type = request.data.pop('type')
        type_data = {"type": p_type}
        type_serializer = UserprofileTypeSerializer(data=type_data)
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
            profile_data = {
                'user': saved_account.id,
                'type': p_type,
                'username': saved_account.username,
                'email': saved_account.email
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("profile_serializer.errors",profile_serializer.errors)
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print("request data", request.data)

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
