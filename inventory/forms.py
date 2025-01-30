from django import forms
from . models import InventorySetting



# Inventory Configurations
class InventoryForm(forms.ModelForm):
    """ Set up your inventory`Name`, `Address` and so on """
    class Meta:
        model = InventorySetting
        widgets = {
            "email":forms.EmailInput(attrs={"class":"form-control", "type":"email"}),
            "logo":forms.FileInput(attrs={"class":"form-control", "type":"file"})
        }
        fields = [
            "name", "logo", "address", "email", "web_address", "phone1", "phone2"
        ]