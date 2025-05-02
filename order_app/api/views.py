from rest_framework.response import Response
from rest_framework import filters, status, generics
from order_app.models import Order, User
from offer_app.models import OfferDetails
from .serializers import OrderSerializer, OrderCountSerializer, CompletedOrderCountSerializer
from .functions import create_new_order
from .permissions import EditOrderPermission
from review_app.api.permissions import IsCustomerPermission

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
