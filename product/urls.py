from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.index, name='search'),
    path('<int:product_id>/', views.detail, name='details'),
]