from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from review_app.models import Review


def set_user_profile(profile_data):
    """
    Creates a user profile using the provided profile data.
    Saves the profile if the data is valid and returns the serialized data.
    Returns error details if the data is invalid.
    """
    serializer = UserProfileSerializer(data=profile_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def get_rating_average(reviews_count):
    """
    Calculates the average rating from a dynamic number of reviews.
    Fetches all reviews, extracts their ratings, and computes the average rating.
    Returns the average rating rounded to one decimal place.
    """
    ratings = []
    reviews = Review.objects.all()
    rating_sum = 0
    for i in range(reviews_count):
        review = reviews[i]
        rating = review.rating
        ratings.append(rating)
        print("len(ratings)",len(ratings))
    for rating in ratings:
        rating_sum += rating
        print("rating_sum", rating_sum)
        review_rating_average = round(rating_sum / len(ratings), 1)
    return review_rating_average