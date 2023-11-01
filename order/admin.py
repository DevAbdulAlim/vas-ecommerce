from django.contrib import admin
from django.urls import reverse
from .models import Order, OrderItem
from payment.models import Address, Payment
from django.utils.html import format_html

#Actions
@admin.action(description="Mark as Delivered")
def mark_delivered(modeladmin, request, queryset):
    queryset.update(status="delivered")
    
def generate_and_print_invoice(modeladmin, request, queryset):
    for order in queryset:
        order.generate_and_print_invoice()
        
generate_and_print_invoice.short_description = "Generate and Print Invoice for Selected Orders"


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
    list_display = ('id','user', 'status', 'total_items', 'subtotal_price', 'total_price', 'print_invoice_link')
    list_display_links = ('id',)
    search_fields = ('user__username',)
    list_filter = ('status',)
    list_editable = ('status',)
    actions = [mark_delivered, generate_and_print_invoice]
    readonly_fields = ['subtotal_price', 'total_price']
    list_per_page = 10
    list_max_show_all = 100



    
    def print_invoice_link(self, obj):
        if obj.is_processed and hasattr(obj, 'invoice'):
            url = reverse('order:print_invoice', args=[obj.invoice.pk])
            return format_html('<a href="{}" target="_blank">Print Invoice</a>', url)
        return ""
    print_invoice_link.short_description = "Print Invoice"

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'get_unit_price', 'item_total_price')

    search_fields = ('order__id',)

    list_filter = ('order',)

    def get_unit_price(self, obj):
        return obj.product.price
    get_unit_price.short_description = "Unit Price"
    
    def add_button(self, obj):
        return '<button class="custom-button" type="button">Custom Button</button>'

    add_button.short_description = 'Custom Action'  # Column heade

# Register to admin model

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
