from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
]