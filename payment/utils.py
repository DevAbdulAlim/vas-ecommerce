def calculate_shipping_charges(order):
    # Perform shipping charge calculation logic here
    shipping_charges = 10 # Example: Fixed shipping charge of $10
    return shipping_charges

def calculate_tax(order):
    # Perform tax calculation logic here
    tax_percentage = 0.1 # Example: 10% tax rate
    tax_amount = order.subtotal_price * tax_percentage
    return tax_amount

def calculate_discount(order):
    # Perform discount calculation logic here
    discount_percentage = 0.2
    discount_amount = order.subtotal_price * discount_percentage
    return discount_amount

def calculate_total_price(order, shipping_charges, tax_amount, discount_amount):
    # Perform total calculation logic here
    total_price = order.subtotal_price + shipping_charges + tax_amount - discount_amount
    return total_price