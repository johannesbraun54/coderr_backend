from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import UserProfile, Offer, OfferDetails, Review, Order
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer, ReviewSerializer, OrderSerializer
from .functions import validate_offer_details, get_detail_keyfacts, create_new_order
from .paginations import LargeResultsSetPagination
from .permissions import IsOwnerPermission, IsBusinessUserPermission, IsCustomerPermission, ReviewPatchPermission, EditOrderPermission


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


class ProfileBusinessListView(GenericAPIView, ListModelMixin):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfileCustomerListView(GenericAPIView, ListModelMixin):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

################################################ OFFER_VIEWS ################################################


class OffersView(GenericAPIView, ListModelMixin):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsBusinessUserPermission]
    filterset_fields = ['user', 'min_price', 'max_delivery_time']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request):
        obj = request.data
        self.check_object_permissions(self.request, obj)
        request.data['user'] = request.user.id
        get_detail_keyfacts(request)
        details = request.data['details']
        serializer = OffersSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            saved_offer = serializer.save()
            validate_offer_details(details, saved_offer.id, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleOfferView(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):

    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    permission_classes = [IsOwnerPermission]

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OfferDetailView(GenericAPIView, RetrieveModelMixin, CreateModelMixin):

    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


################################################ REVIEW_VIEWS ################################################

class ReviewsListView(GenericAPIView, ListModelMixin):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomerPermission]

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request):
        obj = request.data
        request.data['reviewer'] = request.user.id
        self.check_object_permissions(self.request, obj)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("serializer.errors", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPatchPermission]
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


################################################ ORDER_VIEWS ################################################

class OrdersView(GenericAPIView, ListModelMixin):

    permission_classes = [IsCustomerPermission]

    def get(self, request, *args, **kwargs):
        user_type = getattr(request.user.userprofile, 'type', None)
        if user_type == 'customer':
            orders = Order.objects.filter(customer_user=request.user)
        elif user_type == 'business':
            orders = Order.objects.filter(business_user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        obj = request.data
        self.check_object_permissions(self.request, obj)
        create_new_order(request)
        if not create_new_order(request):
            return Response({'error': 'OfferDetail not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersDetailView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [EditOrderPermission]

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderInProgressCountView(GenericAPIView):

    def get(self, request, pk):
        order_count = Order.objects.filter(
            business_user_id=pk, status="in_progress")
        data = {"order_count": len(order_count)}
        return Response(data)


class OrderCompleteCountView(GenericAPIView):

    def get(self, request, pk):
        order_count = Order.objects.filter(
            business_user_id=pk, status="completed")
        data = {"completed_order_count": len(order_count)}
        return Response(data)


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
