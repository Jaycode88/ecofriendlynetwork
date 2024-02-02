from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, DecimalField
from django.contrib import messages
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime

from products.models import Product, Favorite, Category
from checkout.models import OrderLineItem, Order
from .forms import OrderSearchForm


@login_required
def sales_stats(request):
    """
    Display sales statistics for products.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the sales statistics page.
    """
    if not request.user.is_superuser:
        messages.error(
            request, "Access denied. Only superusers can view statistics.")
        return redirect('home')

    # Retrieve filter parameters from GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_product = request.GET.get('product')
    selected_category = request.GET.get('category')

    # Parsing dates
    if start_date:
        start_date = parse_date(start_date)
        start_date = timezone.make_aware(
            datetime.combine(start_date, datetime.min.time()))
    else:
        start_date = timezone.make_aware(datetime(year=2023, month=12, day=1))

    if end_date:
        end_date = parse_date(end_date)
        end_date = timezone.make_aware(
            datetime.combine(end_date, datetime.max.time()))
    else:
        end_date = timezone.now()

    # Getting all products and categories for dropdowns
    products = Product.objects.all()
    categories = Category.objects.all()

    # Base query for products
    query = Product.objects.all()

    # Applying date filter and calculating statistics
    query = query.annotate(
        total_sales=Coalesce(
            Sum('orderlineitem__quantity',
                filter=Q(
                    orderlineitem__order__date__gte=start_date,
                    orderlineitem__order__date__lte=end_date
                )
                ),
            0
        ),

        total_revenue=Coalesce(
            Sum('orderlineitem__lineitem_total',
                filter=Q(
                    orderlineitem__order__date__gte=start_date,
                    orderlineitem__order__date__lte=end_date
                )
                ),
            0,
            output_field=DecimalField()
        ),

        total_favorites=Count('favorite', distinct=True)
    )

    # Applying product filter if selected
    if selected_product:
        query = query.filter(id=selected_product)

    # Applying category filter if selected
    if selected_category:
        query = query.filter(category_id=selected_category)

    sales_and_favorites_data = query

    # Check if the filtered query returns no results and display toast
    if not sales_and_favorites_data.exists():
        messages.warning(request, "No data found for the selected criteria.")

    context = {
        'sales_data': sales_and_favorites_data,
        'products': products,
        'categories': categories,
        'selected_product': selected_product,
        'selected_category': selected_category,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'sales_stats/sales_stats.html', context)


@login_required
def manage_orders(request):
    """
    Display and manage orders with filters.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response containing the manage orders page.
    """
    if not request.user.is_superuser:
        messages.error(
            request, "Access denied. Only superusers can manage orders.")
        return redirect('home')

    # Create an order search form
    form = OrderSearchForm(request.GET)
    query = Order.objects.select_related('user_profile')

    # Retrieve query parameters
    order_number = request.GET.get('order_number')
    username = request.GET.get('username')
    postcode = request.GET.get('postcode')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Adjusting start_date to beginning of the day
    if start_date:
        start_date = parse_date(start_date)
        start_date = timezone.make_aware(
                datetime.combine(start_date, datetime.min.time()))

    # Adjusting end_date to include the entire day up to 23:59:59
    if end_date:
        end_date = parse_date(end_date)
        end_date = timezone.make_aware(
                datetime.combine(end_date, datetime.max.time()))

    # Apply filters if values are provided
    if order_number:
        query = query.filter(order_number__icontains=order_number)
    if username:
        query = query.filter(user_profile__user__username__icontains=username)
    if postcode:
        query = query.filter(postcode__icontains=postcode)
    if start_date:
        query = query.filter(date__gte=start_date)
    if end_date:
        query = query.filter(date__lte=end_date)

    # Retrieve orders based on applied filters
    orders = query.all()

    # Check if the filtered orders query returns no results and display toast
    if not orders:
        messages.warning(
            request, "No orders found matching your search criteria.")

    context = {
        'form': form,
        'orders': orders,
        'order_number': order_number,
        'username': username,
        'postcode': postcode,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'sales_stats/manage_orders.html', context)


@login_required
def order_detail(request, order_id):
    """
    Display order details.

    Args:
        request (HttpRequest): The request object.
        order_id (int): ID of the order.

    Returns:
        HttpResponse: The response containing the order detail page.
    """
    if not request.user.is_superuser:
        messages.error(
            request, "Access denied. Only superusers can view order details.")
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_admin': True,
    }

    return render(request, template, context)
