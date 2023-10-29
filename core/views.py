from django.shortcuts import render
from django.views import View
from product.models import Category, Product


# Create your views here.
class ListView(View):
    def get(self, request):
        categories = Category.objects.all()[:12]
        products = Product.objects.all()[:12]
        return render(request, 'core/index.html', {'categories': categories, 'products': products})
    

