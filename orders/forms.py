from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_type', 'payment_method']




class OrderFilterForm(forms.Form):
    customer_type = forms.ChoiceField(choices=Order.CUSTOMERS_TYPE, required=False)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD, required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))