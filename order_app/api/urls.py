from django.urls import path
from .views import OrdersView, OrdersDetailView, OrderInProgressCountView, OrderCompleteCountView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders-detail'),
    path('order-count/<int:pk>/', OrderInProgressCountView.as_view(), name="orders-count"),
    path('completed-order-count/<int:pk>/', OrderCompleteCountView.as_view(), name="orders-complete-count"),
]
