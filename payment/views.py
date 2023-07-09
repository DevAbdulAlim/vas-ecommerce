from django.conf import settings
from django.shortcuts import render, redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        try:
            # Process the payment using the payment_method_id and perform any necessary business logic
            # You can use the Stripe API to create a charge, subscription, or perform other actions
            # Replace the following code with your actual payment processing logic
            stripe.PaymentIntent.create(
                payment_method=payment_method_id,
                amount=1000,
                currency='usd',
                confirm=True,
            )
            
            return redirect('payment:payment_success')  # Redirect to your own success page
            
        except stripe.error.CardError as e:
            # Handle specific card errors
            error_message = e.user_message
            return render(request, 'payment/payment.html', {'error_message': error_message})
        
        except stripe.error.StripeError:
            # Handle other Stripe errors
            error_message = "An error occurred while processing the payment. Please try again later."
            return render(request, 'payment/payment.html', {'error_message': error_message})

    return render(request, 'payment/payment.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})

def payment_success_view(request):
    return render(request, 'payment/payment_success.html')
