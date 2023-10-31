from django.urls import path
from .views import AddAddress, PaymentView, CashPayment, CardPayment,  PlaceOrder

app_name = 'payment'
urlpatterns = [
    path('address/', AddAddress.as_view(), name='address' ),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/cash', CashPayment.as_view(), name='payment_cash'),
    path('payment/card', CardPayment.as_view(), name='payment_card'),
    path('review/', PlaceOrder.as_view(), name='review'),
]