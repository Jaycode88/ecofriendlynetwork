from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse)
from django.contrib import messages
from products.models import Product

from products.models import Product


def view_bag(request):
    """
    A view to return the shopping bag page with contents.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered shopping bag page with bag contents.
    """

    template = 'bag/bag.html'
    context = {
        'on_bag_page': True,
    }

    return render(request, template, context)

    return render(request, )


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the product to add to the bag.

    Returns:
        HttpResponse: Redirect to the previous page after adding
        the product to the bag.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request, f'Updated {product.name} in your bag to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product in the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the product to adjust.

    Returns:
        HttpResponse: Redirect to the shopping bag view after
        adjusting the quantity.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the specified item from the shopping bag.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the product to remove from the bag.

    Returns:
        HttpResponse: A response indicating the status of the
        removal operation.
    """

    bag = request.session.get('bag', {})
    product = get_object_or_404(Product, pk=item_id)
    try:

        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
