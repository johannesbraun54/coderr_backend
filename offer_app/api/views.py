from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from offer_app.models import Offer, OfferDetails
from .serializers import OffersSerializer, OfferDetailsSerializer, OfferImageUploadSerializer, OfferListSerializer, OfferRetrieveSerializer
from .functions import set_offer_min_price, set_offer_min_delivery_time, set_user_details
from .paginations import LargeResultsSetPagination
from .permissions import IsBusinessUserPermission
from .filters import OfferFilter

class OfferImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = OfferImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get_serializer(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        offer_detail =  OfferDetails.objects.get(pk=pk)
        if self.request.method == 'GET':
            serializer = OfferDetailsSerializer(offer_detail, fields=('id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type'))
            return serializer