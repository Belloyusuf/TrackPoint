from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import sweetify



def cart_add(request, product_id):
    """Add product to cart with stock validation and proceed without success message."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartAddProductForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity > product.quantity_in_stock:
                sweetify.error(request, f"Only {product.quantity_in_stock} items available in stock.")
                return redirect('product_app:product-detail', id=product.id, slug=product.slug)

            cart.add(product=product, quantity=quantity, override_quantity=form.cleaned_data['override'])

            #  Redirect directly to the cart detail page (no success message)
            return redirect('cart_app:cart-detail')

    return redirect('product_app:product-detail', id=product.id, slug=product.slug)




# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
#     return redirect('cart_app:cart-detail')



@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_app:cart-detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})
