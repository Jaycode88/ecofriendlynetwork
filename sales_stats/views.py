from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime

from products.models import Product, Favorite, Category
from checkout.models import OrderLineItem

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