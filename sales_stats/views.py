from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime

from products.models import Product, Favorite, Category
from checkout.models import OrderLineItem, Order
from .forms import OrderSearchForm

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def sales_stats(request):
    start_date = request.GET.get('start_date')
    start_date = parse_date(start_date) if start_date else timezone.make_aware(datetime(year=2023, month=12, day=1))

    end_date = request.GET.get('end_date')
    end_date = parse_date(end_date) if end_date else timezone.now()

    selected_product = request.GET.get('product')
    selected_category = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    # Building the query for sales and favorites data combined
    query_filter = Q(orderlineitem__order__date__gte=start_date, orderlineitem__order__date__lte=end_date) | \
                   Q(favorite__created__gte=start_date, favorite__created__lte=end_date)

    if selected_product:
        query_filter &= Q(id=selected_product)
    if selected_category:
        query_filter &= Q(category_id=selected_category)

    sales_and_favorites_data = Product.objects.annotate(
    total_sales=Coalesce(Sum('orderlineitem__quantity', filter=Q(orderlineitem__order__date__gte=start_date, orderlineitem__order__date__lte=end_date)), 0),
    total_revenue=Coalesce(Sum('orderlineitem__lineitem_total', filter=Q(orderlineitem__order__date__gte=start_date, orderlineitem__order__date__lte=end_date)), 0, output_field=DecimalField()),
    total_favorites=Coalesce(Count('favorite'), 0)
    )

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
@user_passes_test(is_superuser)
def manage_orders(request):
    form = OrderSearchForm(request.GET)
    query = Order.objects.select_related('user_profile')

    # Retrieve query parameters
    order_number = request.GET.get('order_number')
    username = request.GET.get('username')
    postcode = request.GET.get('postcode')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply filters if values are provided
    if order_number:
        query = query.filter(order_number__icontains=order_number)
    if username:
        query = query.filter(user_profile__user__username__icontains=username)
    if postcode:
        query = query.filter(postcode__icontains=postcode)
    if start_date:
        start_date = parse_date(start_date)
        query = query.filter(date__gte=start_date)
    if end_date:
        end_date = parse_date(end_date)
        query = query.filter(date__lte=end_date)

    orders = query.all()

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
@user_passes_test(is_superuser)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_admin': True,
    }

    return render(request, template, context)
