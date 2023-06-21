from django.contrib import admin
from .models import Category, Product


# Customization here
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)
    list_filter = ('category', )
    
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)