from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Post model.
    Defines how blog posts are displayed in the Django admin interface.
    """

    # Columns to display in the blog post list view within the admin.
    list_display = ('title', 'author', 'created_on', 'updated_on')

    # Search functionality based on title and content.
    search_fields = ['title', 'content']

    # Filtering options based on the creation date.
    list_filter = ('created_on',)

# Registering the Post model with its custom admin class.
admin.site.register(Post, PostAdmin)
