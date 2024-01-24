from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Favorite


class ProductForm(forms.ModelForm):
    """
    Form for adding and editing Product instances.
    """

    class Meta:
        model = Product
        fields = '__all__'  # Includes all fields from the Product model

    # Override default image field with custom clearable file input widget
    image = forms.ImageField(
        label='image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to set up additional properties and behaviors.
        """
        super().__init__(*args, **kwargs)

        # Fetch all categories & set as choices for category field
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        # Set a custom CSS class for all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

            # Set autocomplete attribute
            if field_name == 'name':
                field.widget.attrs['autocomplete'] = 'name'


class FavoriteForm(forms.ModelForm):
    """
    Form for managing user's favorite products.
    """
    class Meta:
        model = Favorite
        fields = ['product']
