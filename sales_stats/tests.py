from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import ProductSalesStats
from products.models import Product
from checkout.models import Order
from datetime import datetime, timedelta

class TestProductSalesStatsModel(TestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00
        )
        # Create ProductSalesStats for the product
        self.sales_stats = ProductSalesStats.objects.create(
            product=self.product,
            total_sales=10,
            total_revenue=1000.00,
            favorites_count=5
        )

    def test_product_sales_stats_str(self):
        # Test the string representation of ProductSalesStats
        self.assertEqual(str(self.sales_stats), f'Sales Stats for {self.product.name}')

class TestSalesStatsViews(TestCase):
    def setUp(self):
        # Create and login as a superuser
        self.superuser = User.objects.create_superuser('superuser', 'superuser@test.com', 'superpassword')
        self.client = Client()
        self.client.login(username='superuser', password='superpassword')

    def test_sales_stats_view(self):
        # Test sales_stats view
        response = self.client.get(reverse('sales_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_stats/sales_stats.html')

    def test_manage_orders_view(self):
        # Test manage_orders view
        response = self.client.get(reverse('manage_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_stats/manage_orders.html')

    def test_order_detail_view(self):
        # Create a test order
        order = Order.objects.create(
            full_name='Test User',
            email='test@test.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            county='Test County',
            date=timezone.now()
        )
        # Test order_detail view
        response = self.client.get(reverse('order_detail', args=[order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
