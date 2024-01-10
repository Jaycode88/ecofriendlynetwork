from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Product model.
    Defines how products are displayed in the Django admin interface.
    """

    # Columns to display in the product list view within the admin.
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    # Default ordering for products in the admin list view.
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Category model.
    Defines how categories are displayed in the Django admin interface.
    """

    # Columns to display in the category list view within the admin.
    list_display = (
        'friendly_name',
        'name',
    )

# Registering the Product and Category models with their respective admin classes.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
