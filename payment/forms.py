from django import forms
from .models import Address

class ShippingAddressForm(forms.ModelForm):
    street = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'street'})
        )
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'})
        )
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'})
        )
    country = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'})
        )
    
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'country']
    
class GatewayForm(forms.ModelForm):
    pass