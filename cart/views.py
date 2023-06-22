from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Cart, CartItem
from product.models import Product
import json

# Create your views here.
class ListCartItem(View):
    def get(self, request):
        cart_items = CartItem.objects.all()
        return render(request, 'cart/index.html', {'cart_items': cart_items})
    
class AddCartItem(View):
    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            # Optionally, you can modify cart_item properties here

            cart_item.save()  # Save the cart_item object

            return redirect('product:details', product_id=product_id)

        except Exception as e:
            return JsonResponse({'success': True, 'message': str(e)})

class UpdateCartItem(View):
    def post(self, request, cart_item_id):
        data = json.loads(request.body)
        action = data.get('action')
        print(action)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found'})

        if action == 'increase':
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action type'})

        cart_item.save()

        return JsonResponse({'success': True, 'message': 'Cart item quantity updated', 'quantity': cart_item.quantity,})

class DeleteCartItem(View):
    def post(self, request, cart_item_id):
        print('delete')
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.delete()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})