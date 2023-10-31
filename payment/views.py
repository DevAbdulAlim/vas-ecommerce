from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart
from order.models import Order
from .models import Address, Payment
from .forms import ShippingAddressForm, GatewayForm
from .utils import calculate_shipping_charges, calculate_tax, calculate_discount, calculate_total_price
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.

class AddAddress(View):
    def get(self, request):
        
        form = ShippingAddressForm()
        return render(request, 'payment/address.html', {'form': form})

    def post(self, request):
        order = Order.objects.filter(user=request.user).latest('created_at')
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address, created = Address.objects.get_or_create(order=order) #created holding True or false if the address was found or not
            address.street = form.cleaned_data['street']
            address.city = form.cleaned_data['city']
            address.state = form.cleaned_data['state']
            address.country = form.cleaned_data['country']
            address.save()

            return redirect('payment:payment')
        
        return render(request, 'payment/address.html', {'form': form})

class PaymentView(View):
    def get(self, request):
        return render(request, 'payment/payment.html')

class CashPayment(View):
    def get(self, request):
        return redirect('order_success')
    
class CardPayment(View):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                # for stripe's product
                # {
                # 'price': 'price_1O7E5RIM0hbfA7lPC0pxAOXt',
                # 'quantity': 1,
                # }
                
                # for dynamic product
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 100,
                        'product_data': {
                            'name': 'Sample Product'
                        }
                    },
                    'quantity': 1,
                }
                ],
              mode='payment',
            success_url = request.build_absolute_uri(reverse('payment:review')),
            cancel_url=request.build_absolute_uri(reverse('core:home')),
        )
        return redirect(session.url, code=303)
    
class PlaceOrder(View):
    def get(self, request):
       return redirect('order_success')


class Review(View):
    def get(self, request):
        return render(request, 'payment/review.html')
        

def placeOrder(request):
    # Assuming the authenticated user is accessing this view
    user = request.user

    # Retrieve the most recent order for the user based on the creation timestamp
    order = Order.objects.filter(user=user).latest('created_at')

    if request.method == 'POST':

        # Update the order status or any other relevant fields to indicate that 
        order.status = 'Placed'
        order.save()

        # Perform additional order processing or bussiness logic
        # ...

        # Send order confimation emails or notifications (optional)
        # ...

        # Redirect the user to a success page or show a success message
        return redirect('order_success')



    shipping_charges = calculate_shipping_charges(order)
    tax_amount = calculate_tax(order)
    discount_amount = calculate_discount(order)

    # Calculate the total price by adding the product prices and applying discounts
    total_price = calculate_total_price(order, shipping_charges, tax_amount, discount_amount)

    # Update the order instance with the calculated values
    order.shipping_charges = shipping_charges
    order.tax_amount = tax_amount
    order.discount_amount = discount_amount
    order.total_price = total_price
    order.save()

    
    return render(request, 'checkout/place-order.html', {'order': order})