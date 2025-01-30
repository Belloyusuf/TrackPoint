from django.shortcuts import render
from django.urls import reverse_lazy
from . models import InventorySetting
from . forms import InventoryForm
from sweetify.views import SweetifySuccessMixin
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView



# Inventory Settings
class InventoryCreateView(SweetifySuccessMixin, CreateView):
    """ Sets your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_create.html"
    success_message = "Inventory Created Successfully"
    success_url = reverse_lazy("product_app:inventory-create")
