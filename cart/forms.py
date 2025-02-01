from django import forms



PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',  # Adjust the class for resizing
            'style': 'width: 80px;'  # You can adjust the width here
        })
    )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
