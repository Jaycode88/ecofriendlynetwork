from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """

    # Retrieves the user's profile or 404 if not found.
    profile = get_object_or_404(UserProfile, user=request.user)

    # Handles form submission for profile updates.
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Saves the updated profile information.
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            # Provides an error message if the form is invalid.
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        # Provide form populated with user's profile information.
        form = UserProfileForm(instance=profile)

    # Retrieves all orders associated with the profile.
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'form': form,
        'on_profile_page': True,
    }

    # Renders the profile template with the given context.
    return render(request, template, context)

@login_required
def delete_profile(request):
    """Allows a user to delete their profile."""
    if request.method == "POST":
        user = request.user
        user.delete()  # deletes the User and related UserProfile due to CASCADE
        logout(request)
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect(reverse('home'))  # Redirect to homepage
    else:
        return render(request, 'profiles/delete_profile_confirm.html')


def order_history(request, order_number):
    """ Display the user's past order confirmation. """

    # Retrieves the specified order or 404 if not found.
    order = get_object_or_404(Order, order_number=order_number)

    # Provides an informational message about the past order.
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    # Renders the checkout success template to display the order details.
    return render(request, template, context)
