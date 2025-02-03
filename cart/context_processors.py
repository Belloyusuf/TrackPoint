# cart/context_processors.py
from .cart import Cart  # Assuming you have a cart.py file for cart logic

def cart(request):
    """
    Adds the current cart to the context for use in templates.
    """
    print("Cart context processor called!")
    cart = Cart(request)  # Assuming Cart is a class handling the cart logic
    return {
        'cart': cart  # Pass the cart object to the context
    }
