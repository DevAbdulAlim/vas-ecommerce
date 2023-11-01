from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User
from django.apps import apps

# Create your models here.
class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('canceled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
choices=STATUS_CHOICES, default='pending')
    total_items = models.PositiveIntegerField(null=True, blank=True)
    shipping_charges = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    tax_amount = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    subtotal_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2, default=0)
    total_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    is_processed = models.BooleanField(default=False)

  
    def generate_and_print_invoice(self):
        invoice = Invoice(order=self)
        invoice.save()
        return "Invoice generated for order {} and opened in a new tab for printing.".format(self.pk)

    def calculate_subtotal_price(self, item):
        order_item = self.orderitem_set.get(pk=item)
        self.subtotal_price += order_item.item_total_price
        self.save()
    
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
            Cart = apps.get_model('cart', 'Cart')
            Product = apps.get_model('product', 'Product')
            cart = Cart.objects.get(user=self.user)

            for cart_item in cart.cartitem_set.all():
                # Transfer cart items to order itmes
                OrderItem.objects.create(order=self, product=cart_item.product, quantity=cart_item.quantity)

                # Minus Product stock
                product = Product.objects.get(id = cart_item.product.id)
                product.stock = cart_item.product.stock - cart_item.quantity
                product.save()
            cart.cartitem_set.all().delete()

    def __str__(self):
        # return str(self.user) # Return the string representation cause user is a relatinal field
        return str(self.id)

   

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.product.name
    

    
    @property
    def item_total_price(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total_items()
        self.order.calculate_subtotal_price(self.pk)


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=10)
    # Add other invoice fields
    
    def __str__(self):
        return self.invoice_number