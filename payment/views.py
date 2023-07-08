from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart
from order.models import Order
from .models import Address, Payment
from .forms import ShippingAddressForm, GatewayForm
from .utils import calculate_shipping_charges, calculate_tax, calculate_discount, calculate_total_price


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

class AddGateway(View):
    def get(self, request):
        return render(request, 'payment/payment.html')
    
    def post(self, request):
        return redirect('payment:review')
    
class PlaceOrder(View):
    def get(self, request):
        return render(request, 'payment/review.html')

def addGateway(request):
    if request.method == 'POST': 
        user = request.user

        # You can use order id passing through url paremeter or use teh latest filter for filtering out the latest order placed by the user
        order = Order.objects.filter(user=user).latest('created_at')

        form = GatewayForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                order = order,
                payment_method = form.cleaned_data['payment_method'],
                card_number = form.cleaned_data['card_number'],
                expiry_date = form.cleaned_data['expiry_date'],
            )

            payment.save()

            return redirect('place-order')
    else:
        form = GatewayForm()

    return render(request, 'checkout/Gateway.html', {'form': form})

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