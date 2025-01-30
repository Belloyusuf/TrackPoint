from django.urls import path
from . import views


app_name = "inventory_app"

urlpatterns = [
    path("inventory-settings/", views.InventoryCreateView.as_view(), name="inventory-create"),
]
