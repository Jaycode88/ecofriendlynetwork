from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.

    This form is based on the Post model and allows users to create
    or edit blog posts with the specified fields.

    Attributes:
        Meta (class): A nested class within the form that provides metadata.
            In this case, it specifies the model to use and the fields to include.

    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'excerpt']
