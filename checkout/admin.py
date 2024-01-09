from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Order, OrderLineItem

def export_orders_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)

    # Write CSV headers
    writer.writerow(['Order Number', 'Date', 'Full Name', 'Total'])

    # Write data
    for order in queryset:
        writer.writerow([order.order_number, order.date, order.full_name, order.grand_total])

    return response

export_orders_to_csv.short_description = 'Export to CSV'


class OrderLineItemAdminInLine(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class  OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInLine,)

    readonly_fields = ('order_number', 'date',
                        'delivery_cost', 'order_total',
                        'grand_total', 'original_bag', 
                        'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
                'email', 'phone_number', 'country',
                'postcode', 'town_or_city', 'street_address1',
                'street_address2', 'county', 'delivery_cost',
                'order_total', 'grand_total', 'original_bag', 
                        'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'delivery_cost', 'order_total',
                    'grand_total')

    ordering = ('-date',)

    # Enhanced search fields
    search_fields = ('order_number', 'full_name', 'email', 
                     'phone_number', 'postcode', 'town_or_city', 
                     'street_address1', 'street_address2')

    actions = [export_orders_to_csv]

admin.site.register(Order, OrderAdmin)