from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from review_app.models import Review


def set_user_profile(profile_data):
    print(profile_data)
    serializer = UserProfileSerializer(data=profile_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def get_rating_average(reviews_count):
    ratings = []
    reviews = Review.objects.all()
    rating_sum = 0
    for i in range(reviews_count):
        review = reviews[i]
        rating = review.rating
        ratings.append(rating)
    for rating in ratings:
        rating_sum += rating
        review_rating_average = round(rating_sum / len(ratings), 1)
        return review_rating_average