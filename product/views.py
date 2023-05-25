from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    product_list = Product.objects.all()
    return render(request, 'product/products.html', {'products': product_list})