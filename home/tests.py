from django.test import TestCase
from django.urls import reverse

class HomeViewsTestCase(TestCase):

    def test_index_view_exists(self):
        """
        Test to ensure the index view exists and is accessible.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """
        Test to ensure the index view uses the correct template.
        """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')

    def test_index_view_context(self):
        """
        Test to ensure the index view passes the correct context to the template.
        (Modify this if your view passes context)
        """
        response = self.client.get(reverse('home'))
