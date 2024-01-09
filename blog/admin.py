from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on')
    search_fields = ['title', 'content']
    list_filter = ('created_on',)

admin.site.register(Post, PostAdmin)
