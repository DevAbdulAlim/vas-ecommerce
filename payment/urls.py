from django.urls import path
from .views import AddAddress, AddGateway, PlaceOrder

app_name = 'payment'
urlpatterns = [
    path('address/', AddAddress.as_view(), name='address' ),
    path('payment/', AddGateway.as_view(), name='payment'),
    path('review/', PlaceOrder.as_view(), name='review'),
]