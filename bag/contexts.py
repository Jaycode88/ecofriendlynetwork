from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Calculate and return the context data for the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing bag-related context data.
    """

    bag_items = []  # List to store bag items
    total = 0       # Total price of items in the bag
    product_count = 0   # Total count of products in the bag
    bag = request.session.get('bag', {})  # Retrieve bag data from the session

    for item_id, quantity in bag.items():
        # Loop through items in the bag and retrieve product details
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price   # Calculate subtotal for each item
        # Count the quantity of each product in the bag
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        # Calculate delivery cost and remaining amount for free delivery
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0    # Free delivery if total meets the threshold
        free_delivery_delta = 0

    grand_total = delivery + total  # Calculate the final grand total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
