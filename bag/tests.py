from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from products.models import Product

class TestBagViews(TestCase):
    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00
        )

    def test_view_bag(self):
        # Test the view_bag view
        response = self.client.get(reverse('view_bag'))
        # Check for HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Ensure the correct template is used
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        # Test the add_to_bag view to ensure a product can be successfully added to the bag
        # and that the user stays on the same page with a success message.
        redirect_url = reverse('product_detail', args=[self.product.id])
        response = self.client.post(reverse('add_to_bag', args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': redirect_url
        })
        # Check for redirection back to the product detail page.
        self.assertRedirects(response, redirect_url)
        # Check if the product is added to the bag in the session.
        self.assertEqual(self.client.session['bag'], {str(self.product.id): 1})
        # Check for a success message in the response.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Added {self.product.name} to your bag')


    def test_adjust_bag(self):
        # Add a product to the bag first
        self.client.post(reverse('add_to_bag', args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag')
        })
        # Test the adjust_bag view
        response = self.client.post(reverse('adjust_bag', args=[self.product.id]), {
            'quantity': 2
        })
        self.assertRedirects(response, reverse('view_bag'))
        # Check if the quantity is updated in the bag in the session
        self.assertEqual(self.client.session['bag'], {str(self.product.id): 2})

    def test_remove_from_bag(self):
        # Add a product to the bag first
        self.client.post(reverse('add_to_bag', args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag')
        })
        # Test the remove_from_bag view
        response = self.client.post(reverse('remove_from_bag', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        # Check if the product is removed from the bag in the session
        self.assertEqual(self.client.session['bag'], {})
