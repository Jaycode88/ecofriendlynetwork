from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Custom template filter to calculate the subtotal of a product.

    Args:
        price (Decimal): The price of the product.
        quantity (int): The quantity of the product.

    Returns:
        Decimal: The calculated subtotal of the product (price * quantity).
    """
    return price * quantity
