from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile


class TestOrderModel(TestCase):
    def setUp(self):
        # Create a user and check if the profile already exists
        self.user = User.objects.create(username='testuser', email='test@test.com')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        # Create an order
        self.order = Order.objects.create(
            user_profile=self.user_profile, 
            full_name='Test User', 
            email='test@test.com', 
            phone_number='1234567890', 
            country='US', 
            postcode='12345', 
            town_or_city='Test City', 
            street_address1='123 Test Street', 
            county='Test County')

    def test_order_str(self):
        # Test the string representation of Order
        self.assertEqual(str(self.order), self.order.order_number)


class TestOrderLineItemModel(TestCase):
    def setUp(self):
        # Create a user and check if the profile already exists
        self.user = User.objects.create(username='testuser2', email='test2@test.com')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        # Create an order
        self.order = Order.objects.create(
            user_profile=self.user_profile, 
            full_name='Test User 2', 
            email='test2@test.com', 
            phone_number='1234567890', 
            country='US', 
            postcode='12345', 
            town_or_city='Test City 2', 
            street_address1='123 Test Street 2', 
            county='Test County 2')
        # Create a product
        self.product = Product.objects.create(name='Test Product', price=100.00)
        # Create an order line item
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order, 
            product=self.product, 
            quantity=2)

    def test_order_line_item_str(self):
        # Test the string representation of OrderLineItem
        self.assertEqual(str(self.order_line_item), f'SKU {self.product.sku} on order {self.order.order_number}')


class TestCheckoutViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.checkout_url = reverse('checkout')
        # Create and log in a user
        self.user = User.objects.create_user(username='testuser3', email='test3@test.com', password='testpassword')
        self.client.login(username='testuser3', password='testpassword')
        # Create a product
        self.product = Product.objects.create(name='Test Product', price=100.00)

    def test_checkout_page_with_items(self):
        # Simulate adding items to the bag
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

        # Test accessing the checkout page
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)

    def test_checkout_page_without_items(self):
        # Test accessing the checkout page without items in the bag
        response = self.client.get(self.checkout_url)
        # Expect a redirect since the bag is empty
        self.assertEqual(response.status_code, 302)
