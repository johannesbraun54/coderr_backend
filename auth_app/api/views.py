from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from .functions import set_user_profile


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        p_type = request.data.pop('type', None)
        if p_type in ['customer','business']:
            serializer = RegistrationSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                saved_account = serializer.save()
                set_user_profile({'user': saved_account.id, 'type': p_type, 'username': saved_account.username,'email': saved_account.email})
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
