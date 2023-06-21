from django.shortcuts import render, redirect
from cart.models import Cart
from order.models import Order
from .models import Address, Payment
from .forms import ShippingAddressForm, GatewayForm
from .utils import calculate_shipping_charges, calculate_tax, calculate_discount, calculate_total_price


# Create your views here.

def checkout(request):
    # Assuming the authenticated user is accessing this view or you can add authenticate decorator
    user = request.user

    # Retrive the cart for the user
    cart = Cart.objects.get(user=user)

    # Create an order
    order = Order.objects.create(user=user)

    # Transfer items from CartItem to OrderItem
    # have done in the model
    # for cart_item in cart.cartitem_set.all():
    #     OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

    # cart.cartitem_set.all().delete()

    # Perform any additional checkout logic

    # Redirect or rendera success message

def add_shipping_address(request):
     # Assuming the authenticated user is accessing this view or you can add authenticate decorator

    if request.method == 'POST':

        user = request.user

        # You can use order id passing through url paremeter or use the latest filter for filtering out the latest order placed by the user 
        order = Order.objects.filter(user=user).latest('created_at')

        form = ShippingAddressForm(request.POST)
        if form.is_valid():

            # Crate an address and associate it with the order
            address = Address.objects.create(
                order=order,
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                # Add other fields as needed
            )

            address.save()

            return redirect('gateway')
    else:
        form = ShippingAddressForm()
    return render(request, 'shipping_address.html', {'form': form})

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