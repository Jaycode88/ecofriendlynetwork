from django.contrib import admin
from django.http import HttpResponse
import csv
from checkout.models import OrderLineItem  # Import your order model

@admin.action(description='Download Sales Stats')
def download_sales_stats(modeladmin, request, queryset):
    # Logic to calculate and download sales stats
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_stats.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Total Sales', 'Total Revenue'])
    
    for order_item in queryset:
        # Aggregate data and write to CSV
        writer.writerow([order_item.product.name, order_item.quantity, order_item.lineitem_total])
    
    return response

class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'lineitem_total']
    actions = [download_sales_stats]
    list_filter = ('order__date',)
    search_fields = ('order__order_number', 'product__name')

admin.site.register(OrderLineItem, OrderLineItemAdmin)

