from django.contrib import admin
from .models import Cart, CartItem

# inlines here
class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 1


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