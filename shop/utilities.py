from .cart import Cart
from .models import Order, OrderItem
 
    
def checkout(request, full_name,address,zip_code,city,country, amount):
    order = Order.objects.create(
        full_name=full_name,
        address=address,
        zip_code=zip_code,
        country=country,
        city=city,
        user=request.user,
        paid_amount=amount,
        )

    for item in Cart(request):
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            vendor=item['product'].vendor,
            price = item['product'].price,

        )
        order.vendors.add(item['product'].vendor)

    return order    