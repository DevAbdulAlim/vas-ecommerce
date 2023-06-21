from django.contrib import admin
from .models import Profile

# customize model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address',)
    search_fields = ('id', 'phone_number', )

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
