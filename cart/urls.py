from django.urls import path
from .views import ListCartItem, AddCartItem, UpdateCartItem, DeleteCartItem

app_name = 'cart'
urlpatterns = [
    path('', ListCartItem.as_view(), name='list-cart-item'),
    path('add/<int:product_id>/',  AddCartItem.as_view(), name='add-cart-item' ),
    path('update/<int:cart_item_id>/', UpdateCartItem.as_view(), name='update-cart-item'),
    path('delete/<int:cart_item_id>/', DeleteCartItem.as_view(), name='delete-cart-item' ),
]