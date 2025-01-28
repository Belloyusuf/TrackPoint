from django.urls import path
from . import views



app_name = 'product_app'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products', views.ListProducts.as_view(), name='product-list'),
    path("add-product/", views.AddNewProduct.as_view(), name="add-product"),
]
