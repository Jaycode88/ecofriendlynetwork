from django import forms

class OrderSearchForm(forms.Form):
    order_number = forms.CharField(required=False)
    username = forms.CharField(required=False)
    postcode = forms.CharField(required=False)
    date = forms.DateField(required=False)
