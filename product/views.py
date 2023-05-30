from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

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
    product = Product.objects.get(pk=product_id)
    product_list = Product.objects.filter(category = product.category)
    return render(request, 'product/product-detail.html', {'product': product, 'products': product_list})