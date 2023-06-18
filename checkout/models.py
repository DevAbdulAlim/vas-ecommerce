from django.db import models
from core.models import BaseModel
from shopping.models import Order

# Create your models here.

class Address(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Payment(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    expiry_date = models.DateField()



class Coupon(BaseModel):
    pass