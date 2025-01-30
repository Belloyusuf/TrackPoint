from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from . models import InventorySetting
from . forms import InventoryForm
from sweetify.views import SweetifySuccessMixin
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView
import sweetify








# Inventory Settings
class InventoryCreateView(SweetifySuccessMixin, CreateView):
    """ Sets your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_create.html"
    success_message = "Inventory Created Successfully"
    success_url = reverse_lazy("product_app:inventory-create")



    def form_valid(self, form):
        # Save the product
        form.save()
        
        # Show a success toast message
        sweetify.toast(self.request, self.success_message, icon="success")
        
        # Return an empty form to clear the input fields
        return self.render_to_response(self.get_context_data(form=self.form_class()))

    def form_invalid(self, form):
        # If the form is invalid, show an error message
        error_message = form.errors.get('__all__', ['Something went wrong.'])[0]
        sweetify.toast(self.request, error_message, icon="error")
        
        # Return the template with the invalid form data
        return self.render_to_response(self.get_context_data(form=form))
    


    def get(self, request, *args, **kwargs):
        # Check if the Inventory Information Already Exists
        if InventorySetting.objects.exists():
            inventory_info = InventorySetting.objects.first() # Get the first the first or (only) inventory object
            sweetify.toast(self.request, "Inventory Information already Exists. You can only update it.", icon="error")
            return redirect(reverse_lazy("inventory_app:inventory-update", kwargs={'pk':inventory_info.pk}))
        return super().get(request, *args, **kwargs)
    


    def post(self, request, *args, **kwargs):
        # Check if the Inventory Information Already Exists
        if InventorySetting.objects.exists():
            inventory_info = InventorySetting.objects.first() # Get the first the first or (only) inventory object
            sweetify.toast(self.request, "Inventory Information already Exists. You can only update it.", icon="error")
            return redirect(reverse_lazy("inventory_app:inventory-update", kwargs={'pk':inventory_info.pk}))
        return super().post(request, *args, **kwargs)
    


# Update Inventory
class InventoryUpdate(SweetifySuccessMixin, CreateView):
    """ Update your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_update.html"
    success_message = "Inventory Updated Successfully"
    success_url = reverse_lazy("product_app:inventory-update")