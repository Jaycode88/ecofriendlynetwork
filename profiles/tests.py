from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from checkout.models import Order


class TestProfileViews(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(
                username='testuser', password='12345')
        self.user_profile = UserProfile.objects.get(user=self.user)
        # Create a test order for the user
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            order_number='00000001'
        )

    def test_profile_view(self):
        # Log in the test user
        self.client.login(username='testuser', password='12345')
        # Get the response from the profile view
        response = self.client.get(reverse('profile'))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'profiles/profile.html')
        # Check if 'form' and 'orders' are in the response context
        self.assertIn('form', response.context)
        self.assertIn('orders', response.context)

    def test_order_history_view(self):
        # Log in the test user
        self.client.login(username='testuser', password='12345')
        # Get response from order_history view with the test order's number
        response = self.client.get(
            reverse('order_history', args=[self.order.order_number]))
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        # Check if 'order' is in the response context
        self.assertIn('order', response.context)
