from django.urls import path
from . import views


app_name = "inventory_app"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("inventory/", views.InventoryList.as_view(), name="inventory-list"),
    path("inventory-create/", views.InventoryCreateView.as_view(), name="inventory-create"),
    path("inventory-update/<int:pk>/", views.InventoryUpdate.as_view(), name="inventory-update"),
]
