from django.db import models
from products.models import Product

class ProductSalesStats(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sales_stats')
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    favorites_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Sales Stats for {self.product.name}'
