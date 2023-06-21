from django.contrib import admin
from .models import Address, Payment

# Inlines here



# Customize her
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'street', 'city', 'state', 'country',)
    search_fields = ('order',)
    list_filter = ('city', 'country', )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'card_number', 'expiry_date', )
    search_fields = ('order',)
    list_filter = ('payment_method', )


# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment, PaymentAdmin)