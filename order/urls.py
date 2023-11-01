from django.urls import path
from .views import OrderView, PrintInvoice

app_name = 'order'
urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('print_invoice/<int:invoice_id>', PrintInvoice.as_view(), name='print_invoice' ),
]