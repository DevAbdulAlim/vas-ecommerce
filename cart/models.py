from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.
class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
