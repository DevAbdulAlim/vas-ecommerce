from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='initiate')
    total_items = models.PositiveIntegerField(null=True, blank=True)
    shipping_charges = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    tax_amount = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    subtotal_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    total_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

    def calculate_subtotal_price(self):
        subtotal_price = 0
        # Check if there are any order items
        if self.orderitem_set.exists():
            for order_item in self.orderitem_set.all():
                subtotal_price += order_item.item_total_price
        return subtotal_price
    
    def calculate_total_items(self):
        # Check if there are any order items
        if self.orderitem_set.exists():
            self.total_items = self.orderitem_set.count()
            self.save()

    def save(self, *args, **kwargs):

        # Checkif the order is being create (has no primary key yet)
        is_new_order = not self.pk
        
        # Call the parent's save() method to save the order
        super().save(*args, **kwargs)

        # If it's a new order, transfer items from CartItem to OrderItem and delete CartItem
        if is_new_order:
            cart = Cart.objects.get(user=self.user)

            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(order=self, product=cart_item.product, quantity=cart_item.quantity)
            cart.cartitem_set.all().delete()

   

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def item_total_price(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total_items()
        self.order.calculate_subtotal_price()
