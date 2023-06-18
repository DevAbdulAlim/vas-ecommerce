from django.shortcuts import render
import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if 'payment_method_id' in data:
             value = data['payment_method_id']
            # Do something with the value
            print(value)

            # Retrieve payment method ID from the request payload
            # payment_method_id = request.POST['payment_method_id']
            payment_method_id = value
          
           
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # Amount in cents
            currency='usd',
            payment_method_types=['card'],
            payment_method=payment_method_id,
            confirm=True,
            description = "description",
      
            shipping={
                "name": "Jenny Rosen",
                "address": {
                "line1": "510 Townsend St",
                "postal_code": "98140",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
                },
            },
           
        )

 



            # Check if the payment intent status is 'succeeded'
            if payment_intent.status == 'succeeded':
                return JsonResponse({'success': True, 'message': 'Payment succeeded'})
            else:
                # Payment failed
                return JsonResponse({'success': False, 'message': 'Payment failed'})

        except stripe.error.CardError as e:
            # Payment failed
            error_message = e.error.message
            return JsonResponse({'success': False, 'message': error_message})
        except Exception as e:
            # Handle other exceptions
            error_message = str(e)
            return JsonResponse({'success': False, 'message': error_message})

    return JsonResponse({'error': 'Invalid request'})


def payment_view(request):
    STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'payment/payment_form.html', {'STRIPE_PUBLISHABLE_KEY': STRIPE_PUBLISHABLE_KEY})
