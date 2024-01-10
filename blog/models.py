from django.db import models

from django.contrib.auth.models import User

class Post(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the blog post (max length 200 characters).
        author (User): The author of the post, linked to the User model.
        excerpt (str, optional): A short description or excerpt of the blog post (nullable and blank).
        content (str): The main content of the blog post.
        image (ImageField, optional): An image associated with the blog post (nullable and blank).
        created_on (DateTimeField): The date and time when the post was created (auto-generated).
        updated_on (DateTimeField): The date and time when the post was last updated (auto-generated).

    Methods:
        __str__(): Returns the title of the post as its string representation.

    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    excerpt = models.TextField(null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the title of the post as its string representation."""
        return self.title

class Favorite(models.Model):
    """
    Represents a user's favorite blog posts.

    Attributes:
        user (User): The user who has favorite posts, linked to the User model.
        posts (ManyToManyField): A many-to-many relationship with the Post model,
            allowing users to have multiple favorite posts.

    Methods:
        __str__(): Returns a string representation of the user's favorite posts, including the user's username.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_posts")
    posts = models.ManyToManyField(Post)

    def __str__(self):
        """
        Returns a string representation of the user's favorite posts,
        including the user's username.
        """
        return f"{self.user.username}'s favorite posts"
