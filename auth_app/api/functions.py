from coderr_app.api.serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status


def set_user_profile(profile_data):
    serializer = UserProfileSerializer(data=profile_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)