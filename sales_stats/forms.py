from django import forms

class OrderSearchForm(forms.Form):
    """
    Form for searching orders based on various criteria.

    Fields:
        order_number (CharField): Order number input field (optional).
        username (CharField): Username input field (optional).
        postcode (CharField): Postcode input field (optional).
        date (DateField): Date input field (optional).
    """
    
    order_number = forms.CharField(required=False)
    username = forms.CharField(required=False)
    postcode = forms.CharField(required=False)
    date = forms.DateField(required=False)
