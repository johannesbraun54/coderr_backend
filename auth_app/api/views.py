from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserprofileTypeSerializer
from rest_framework.response import Response
from auth_app.models import UserProfile


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        type = request.data.pop('type')
        print("profile_type",type)
        type_serializer = UserprofileTypeSerializer(data=type)
        serializer = RegistrationSerializer(data=request.data)
            

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            print("saved_account",saved_account)
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
            if type_serializer.is_valid():
                profil_type= type_serializer.validated_data.get('type')
                UserProfile.objects.create(user=saved_account, type=profil_type)
            print("saved_account data",data)
        else: 
            data = serializer.errors
        return Response(data)
