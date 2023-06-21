from django.contrib import admin
from .models import Order, OrderItem
from payment.models import Address, Payment



#Inlines
class OrderInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


# Customize Admin models

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline, AddressInline, PaymentInline,]
    list_display = ('id', 'user', 'status', 'total_items', 'subtotal_price', 'total_price')
    search_fields = ('user__username',)
    list_filter = ('status',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'get_unit_price', 'item_total_price')

    search_fields = ('order__id',)

    list_filter = ('order',)

    def get_unit_price(self, obj):
        return obj.product.price
    get_unit_price.short_description = "Unit Price"

# Register to admin model

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
