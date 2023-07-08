from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart
from .models import Order

# Create your views here.
class OrderView(View):
    def get(self, request):
        return render(request, 'order/order.html')

    def post(self, request):
        # Assuming the authenticated user is accessing this view or you can add authenticate decorator
        user = request.user

        # Retrive the cart for the user
        cart = Cart.objects.get(user=user)
       
        if cart.cartitem_set.exists():
            order = Order.objects.create(user=user)
        else:
            return redirect('core:home')

        return redirect('payment:address')