from django.contrib import admin
from .models import Cart, CartItem

# inlines here
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product_price']  
    def product_price(self, instance):
        return instance.product.price

    def has_add_permission(self, request, obj=None):
        return False  # Hide the "Add" button for the read-only field

    product_price.short_description = 'Unit Price'


# custimization here
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, ]
    list_display = ('id', 'user',)
    search_fields = ('user',)
    list_filter = ('user',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')



# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)