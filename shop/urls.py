from django.urls import path
from . import views



app_name = 'product_app'


urlpatterns = [
    # Product urls
    path("products-list", views.ListProducts.as_view(), name="product-list"),
    path("create-product/", views.AddNewProduct.as_view(), name="add-product"),
    path("update-product/", views.UpdateProducts.as_view(), name="update-product"),
    path("delete-product/", views.DeleteProduct.as_view(), name="delete-product"),
    # Category urls
    path("create-category/", views.CreateCategory.as_view(), name="create-category"),
    path("list-category/", views.ListCategories.as_view(), name="list-category"),
    path("update-category/", views.UpdateCategories.as_view(), name="update-category"),
    path("update-category/", views.DeleteCategories.as_view(), name="delete-category"),
]
