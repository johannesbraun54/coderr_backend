from django.urls import path
from .views import ReviewsListView, ReviewsDetailView

urlpatterns = [
    path('reviews/', ReviewsListView.as_view(), name="reviews-list"),
    path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name='reviews-detail'),
]
