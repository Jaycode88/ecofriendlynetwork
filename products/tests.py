from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Favorite
from .forms import ProductForm


class TestCategoryModel(TestCase):
    # Test the string representation and methods of the Category model
    def test_category_str(self):
        # Create a sample category
        category = Category.objects.create(
                name='TestCategory', friendly_name='Test Friendly Name')
        # Check if the string representation matches the category name
        self.assertEqual(str(category), 'TestCategory')
        # Check if the friendly name method returns the expected value
        self.assertEqual(category.get_friendly_name(), 'Test Friendly Name')


class TestProductModel(TestCase):
    # Test the string representation of the Product model
    def test_product_str(self):
        # Create a sample category and product
        category = Category.objects.create(name='TestCategory')
        product = Product.objects.create(
            name='TestProduct', category=category, price=9.99)
        # Check if the string representation matches the product name
        self.assertEqual(str(product), 'TestProduct')


class TestViews(TestCase):
    # Set up initial data for testing views
    def setUp(self):
        # Create a superuser for tests
        self.superuser = User.objects.create_superuser(
                username='testsuperuser', password='12345')
        # Create a test user and a sample product
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct', category=category, price=9.99)

    # Test the all_products view
    def test_all_products_view(self):
        # Get the response from the all_products view
        response = self.client.get(reverse('products'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'products/products.html')
        # Check if 'products' is in the response context
        self.assertIn('products', response.context)

    # Test the product_detail view
    def test_product_detail_view(self):
        # Get response from product_detail view with the test product's ID
        response = self.client.get(
            reverse('product_detail', args=[self.product.id]))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'products/product_detail.html')
        # Check if 'product' is in the response context
        self.assertIn('product', response.context)

    # Test the add_product view for non superuser
    def test_add_product_view(self):
        # Log in as the test user
        self.client.login(username='testuser', password='12345')
        # Get the response from the add_product view
        response = self.client.get(reverse('add_product'))
        # Check if the response status code is 302 redirect
        self.assertEqual(response.status_code, 302)

    # Test the add_product view for a superuser
    def test_add_product_view_superuser(self):
        # Log in as the superuser
        self.client.login(username='testsuperuser', password='12345')
        # Get the response from the add_product view
        response = self.client.get(reverse('add_product'))
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'products/add_product.html')


class TestProductForm(TestCase):
    # Test the ProductForm
    def test_product_form(self):
        # Create form data for a new product
        form_data = {
            'name': 'TestProduct',
            'description': 'Test description',
            'price': 10.00,
        }
        # Create an instance of ProductForm with the form data
        form = ProductForm(data=form_data)
        # Check if the form is valid
        self.assertTrue(form.is_valid())


class TestFavoriteModel(TestCase):
    # Test the string representation of the Favorite model
    def test_favorite_str(self):
        # Create a test user, category, product, and favorite
        user = User.objects.create_user(username='testuser', password='12345')
        category = Category.objects.create(name='TestCategory')
        product = Product.objects.create(
                name='TestProduct', category=category, price=9.99)
        favorite = Favorite.objects.create(user=user, product=product)
        # Check if the string representation matches the expected format
        self.assertEqual(str(favorite), "testuser's favorite TestProduct")
