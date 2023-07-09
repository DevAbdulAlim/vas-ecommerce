from django.conf import settings
from django.shortcuts import render, redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    if request.method == 'POST':
        # Generate test token using the Stripe test card details
        test_token = 'tok_visa'  # Replace with the test token generated for your desired test card

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Product Name',
                            },
                            'unit_amount': 1000,  # Amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://www.google.com/',  # Replace with your success URL
                cancel_url='http://yourwebsite.com/payment/cancel/',  # Replace with your cancel URL
            )

            return redirect(session.url)

        except stripe.error.CardError as e:
            error_message = e.user_message
            return render(request, 'payment/payment.html', {'error_message': error_message})

    return render(request, 'payment/payment.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_secret_key': settings.STRIPE_SECRET_KEY
    })

def payment_success_view(request):
    return render(request, 'payment/payment_success.html')
