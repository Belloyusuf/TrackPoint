from django import forms
from . models import Product, Category
from django.core.exceptions import ValidationError









# Product Form
class ProductForm(forms.ModelForm):
    """ Form that would handle product's creation """
    class Meta:
        model = Product
        widgets ={
            "expiry_date":forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        fields = [
            "name", "category", "image", "description", 
            "barcode", "cost_price", "selling_price", 
            "shelf", "quantity_in_stock", "expiry_date", 
            "unit_of_measurement"
        ]

        def clean(self):
            cleaned_data = super().clean()

            cost_price = cleaned_data.get('cost_price')
            selling_price = cleaned_data.get('selling_price')

            if selling_price <= cost_price:
                raise ValidationError("Selling price must be greater than cost price.")

            return cleaned_data
        



