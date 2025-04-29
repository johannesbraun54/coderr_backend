from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import UserProfile, Offer, OfferDetails, Review, Order, User
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer, ReviewSerializer, OrderSerializer, OrderCountSerializer, CompletedOrderCountSerializer
from .functions import create_new_order, set_offer_min_price, set_offer_min_delivery_time, get_rating_average
from .paginations import LargeResultsSetPagination
from .permissions import IsOwnerPermission, IsBusinessUserPermission, IsCustomerPermission, ReviewPatchPermission, EditOrderPermission
from .filters import OfferFilter


################################################ IMAGEUPLOAD_VIEWS ################################################

class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = OfferImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################ PROFILE_VIEWS ################################################


class ProfileView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    permission_classes = [IsOwnerPermission]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ProfileBusinessListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserProfileSerializer


class ProfileCustomerListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserProfileSerializer

################################################ OFFER_VIEWS ################################################

class OffersView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsBusinessUserPermission]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        min_price=set_offer_min_price(self.request.data['details']), 
                        min_delivery_time=set_offer_min_delivery_time(self.request))


class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    permission_classes = [IsOwnerPermission]


class OfferDetailView(GenericAPIView, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin):

    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


################################################ REVIEW_VIEWS ################################################

class ReviewsListView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomerPermission]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPatchPermission]
    lookup_field = "pk"


################################################ ORDER_VIEWS ################################################

class OrdersView(generics.ListCreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsCustomerPermission]

    def get_queryset(self):
        user_type = getattr(self.request.user.userprofile, 'type', None)
        if user_type == 'customer':
            queryset = Order.objects.filter(customer_user=self.request.user)
        elif user_type == 'business':
            queryset = Order.objects.filter(business_user=self.request.user)
        return queryset

    def post(self, request):
        serializer = OrderSerializer(data=create_new_order(request))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [EditOrderPermission]


class OrderInProgressCountView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = OrderCountSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        queryset = User.objects.filter(userprofile__type='business', pk=pk)
        return queryset


class OrderCompleteCountView(OrderInProgressCountView):

    serializer_class = CompletedOrderCountSerializer




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
