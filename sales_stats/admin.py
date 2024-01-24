from django.contrib import admin
from django.http import HttpResponse
import csv
from checkout.models import OrderLineItem


@admin.action(description='Download Sales Stats')
def download_sales_stats(modeladmin, request, queryset):
    """
    Custom admin action to download sales statistics as a CSV file.
    It aggregates sales data and creates a CSV file for download.

    Args:
        modeladmin: The admin instance.
        request: The request object.
        queryset: The queryset containing OrderLineItem objects.

    Returns:
        HttpResponse: A CSV file response containing sales statistics.
    """

    # Logic to calculate and download sales stats
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_stats.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Total Sales', 'Total Revenue'])

    for order_item in queryset:
        # Aggregate data and write to CSV
        writer.writerow(
            [order_item.product.name, order_item.quantity,
                order_item.lineitem_total])

    return response
