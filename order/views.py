from django.shortcuts import render
from django.views import View

# Create your views here.
class OrderView(View):
    def get(self, request):
        return render(request, 'order/order.html')

    def post(self, request):
        pass