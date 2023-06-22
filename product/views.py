from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from .models import Product, Category
from cart.models import Cart, CartItem

# Create your views here.
def index(request):
    selected_category = None
    selected_min_price = 0
    selected_max_price = 100000
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_min_price = request.POST.get('min_price', 0)
        selected_max_price = request.POST.get('max_price')

        filters = Q()
        if selected_category:
            filters &= Q(category__name=selected_category)
            
        if selected_min_price:
            filters &= Q(price__gte=selected_min_price)

        if selected_max_price:
            filters &= Q(price__lte=selected_max_price)

        product_list = Product.objects.filter(filters)
    else:
        product_list = Product.objects.all()

    category_list = Category.objects.all()
    return render(request, 'product/products.html', {'products': product_list, 'categories': category_list, 'selected_category': selected_category, 'selected_min_price': selected_min_price, 'selected_max_price': selected_max_price})

def detail(request, product_id):
    cart_item = None
    product = get_object_or_404(Product, pk=product_id)
    if product:
        product_list = get_list_or_404(Product, category = product.category)

    # Check if the product is alread added to the cart
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
        cart_items = CartItem.objects.filter(cart = cart, product = product_id)
        if cart_items:
           cart_item = cart_items.all()[0]
  


    return render(request, 'product/product-detail.html', {'product': product, 'products': product_list, 'cart_item': cart_item,})