from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from review_app.models import Review
from .serializers import  ReviewSerializer
from .permissions import IsCustomerPermission, ReviewPatchPermission

class ReviewsListView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomerPermission] # wird auch bei order benuzt, ändern?

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPatchPermission]
    lookup_field = "pk"