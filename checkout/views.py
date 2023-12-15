from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51ONcC6ALF2iickIeWDJxeqc1pHLfgLwKM65l77C0qdesHaX1XZXRinOxLg1HjOqp7sStVwSBSlD6PScY3BinVuN300OGiJTvai',
        'client_secret': 'test value',
    }

    return render(request, template, context)
