from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from coderr_app.models import UserProfile, Offer, OfferDetails, Review, Order, User
from .serializers import UserProfileSerializer, OffersSerializer, ImageUploadSerializer, OfferDetailsSerializer, OfferImageUploadSerializer, ReviewSerializer, OrderSerializer, OrderCountSerializer, CompletedOrderCountSerializer, OfferListSerializer, OfferRetrieveSerializer
from .functions import create_new_order, set_offer_min_price, set_offer_min_delivery_time, set_user_details, get_rating_average
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

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerPermission]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'

class ProfileBusinessListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserProfileSerializer

class ProfileCustomerListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserProfileSerializer

################################################ OFFER_VIEWS ################################################

class OffersViewSet(viewsets.ModelViewSet):
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
                        min_delivery_time=set_offer_min_delivery_time(self.request),
                        user_details=set_user_details(self.request.user))
        
    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.kwargs == {}:
                return OfferListSerializer
            else:
                return OfferRetrieveSerializer
        return OffersSerializer





class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer


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
        try:
            offer_detail_id = request.data.get('offer_detail_id', None)
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
            if offer_detail:
                serializer = OrderSerializer(data=create_new_order(request))
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OfferDetails.DoesNotExist:
            error = {'error': 'Offerdetail with the specified Id not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            error = {'error': 'offer_detail_id must be a number'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)





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
