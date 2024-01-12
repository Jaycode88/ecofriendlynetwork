from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        # Define the form using the Order model
        model = Order

        # Specify the fields to include in the form
        fields = ('full_name', 'email', 'phone_number',
                    'street_address1', 'street_address2',
                    'town_or_city', 'postcode',  'country',
                    'county')

    def __init__(self, *args, **kwargs):
        """
        Customize form field attributes, labels, and placeholders
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Set autofocus on the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    # Add an asterisk to required fields
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set placeholder text for the field
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add a custom CSS class to the field
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove the auto-generated labels
            self.fields[field].label = False
