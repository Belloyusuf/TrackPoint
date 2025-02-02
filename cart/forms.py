from django import forms
from django.core.validators import MaxValueValidator  # Import the correct module




class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 80px;',
        })
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        """Dynamically set max value based on product stock"""
        self.product = kwargs.pop('product', None)  # Get product from kwargs
        super().__init__(*args, **kwargs)

        if self.product:
            self.fields['quantity'].validators.append(
                MaxValueValidator(self.product.quantity_in_stock)  # Use correct import
            )