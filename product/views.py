from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    product_list = Product.objects.all()
    return render(request, 'product/products.html', {'products': product_list})

def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_list = Product.objects.filter(category = product.category)
    return render(request, 'product/product-detail.html', {'product': product, 'products': product_list})