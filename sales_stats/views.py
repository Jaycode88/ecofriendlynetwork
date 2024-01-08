from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.utils import timezone
from django.utils.dateparse import parse_date

from products.models import Product, Favorite, Category
from checkout.models import OrderLineItem

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def sales_stats(request):
    # Convert string to date
    start_date = request.GET.get('start_date')
    start_date = parse_date(start_date) if start_date else None
    end_date = request.GET.get('end_date')
    end_date = parse_date(end_date) if end_date else timezone.now()

    # Filters for product and category
    selected_product = request.GET.get('product')
    selected_category = request.GET.get('category')

    # Fetch all products and categories for the dropdowns
    products = Product.objects.all()
    categories = Category.objects.all()

    # Start building the query for sales data
    sales_query = OrderLineItem.objects
    if start_date:
        sales_query = sales_query.filter(order__date__gte=start_date)
    if end_date:
        sales_query = sales_query.filter(order__date__lte=end_date)
    if selected_product:
        sales_query = sales_query.filter(product_id=selected_product)
    if selected_category:
        sales_query = sales_query.filter(product__category_id=selected_category)

    sales_data = sales_query.values('product__name').annotate(total_sales=Sum('quantity'), total_revenue=Sum('lineitem_total'))

    # Aggregate favorites data
    favorites_query = Favorite.objects
    if selected_product:
        favorites_query = favorites_query.filter(product_id=selected_product)
    if selected_category:
        favorites_query = favorites_query.filter(product__category_id=selected_category)

    favorites_data = favorites_query.values('product__name').annotate(total_favorites=Count('id'))

    context = {
        'sales_data': sales_data,
        'favorites_data': favorites_data,
        'products': products,
        'categories': categories,
        'selected_product': selected_product,
        'selected_category': selected_category,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'sales_stats/sales_stats.html', context)