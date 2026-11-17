
# Make the total shopping cart quantity available across all templates
def cart_quantity(request):
    cart = request.session.get('cart', {})

    cart_count = sum(cart.values())

    return {
        'cart_count': cart_count
    }
