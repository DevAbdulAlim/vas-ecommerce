from django.contrib import admin
from .models import Order, OrderItem
from payment.models import Address, Payment

#Actions
@admin.action(description="Mark as Delivered")
def mark_delivered(modeladmin, request, queryset):
    queryset.update(status="delivered")


#Inlines
class OrderInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_price']  
    def product_price(self, instance):
        return instance.product.price

    # def has_add_permission(self, request, obj=None):
    #     return False  # Hide the "Add" button for the read-only field

    product_price.short_description = 'Unit Price'

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


# Customize Admin models

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline, AddressInline, PaymentInline,]
    list_display = ('id','user', 'status', 'total_items', 'subtotal_price', 'total_price')
    search_fields = ('user__username',)
    list_filter = ('status',)
    list_editable = ('status',)
    actions = [mark_delivered]

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
