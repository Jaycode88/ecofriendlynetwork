from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Category model for categorizing products.
    Includes a technical name and a user-friendly name.
    """

    class Meta:
        verbose_name_plural = 'Categories'  # Correct plural form for admin

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        # String representation of the Category, using its technical name
        return self.name

    def get_friendly_name(self):
        # Returns the user-friendly name for display purposes
        return self.friendly_name


class Product(models.Model):
    """
    Product model representing each individual product.
    Contains information such as category, SKU, name, description, etc.
    """

    # ForeignKey to Category. If category is deleted, products set no category.
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    # Optional SKU field
    sku = models.CharField(max_length=254, null=True, blank=True)
    # Product name
    name = models.CharField(max_length=254)
    # Detailed description of the product
    description = models.TextField()
    # Product price
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Optional product rating
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    # Optional URL for product image
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    # Optional image upload field
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        # String representation of the Product, using its name
        return self.name


class Favorite(models.Model):
    """
    Favorite model to track user's favorite products.
    Links between a user and a product.
    """

    # Link to the user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Link to the product
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        # Ensures a user can only favorite a product once
        unique_together = ('user', 'product')

    def __str__(self):
        # String representation showing the user and the favorited product
        return f"{self.user.username}'s favorite {self.product.name}"
