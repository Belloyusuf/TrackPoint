from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from . models import Order
from django.urls import reverse
from inventory.models import InventorySetting



# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # clear the cart
#             cart.clear()
#             # launch asynchronous task
#             # order_created.delay(order.id)
#             # return render(request,
#             #               'orders/order/setbill.html',
#             #               {'order': order})
#             return redirect('orders:payment')
#     else:
#         form = OrderCreateForm()
#     return render(request,
#                   'orders/create_order.html',
#                   {'cart': cart, 'form': form})



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Clear the cart
            cart.clear()
            
            # Redirect to the invoice page with the order ID
            return redirect(reverse('orders:invoice', args=[order.id]))

    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form})



# Invoice 
def order_invoice(request, order_id):
    inventory = InventorySetting.objects.first()
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/invoice.html', {'order': order, 'inventory':inventory})