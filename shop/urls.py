from django.urls import path
from . import views



app_name = 'product_app'


urlpatterns = [
    # Product urls
    path("products-list", views.ProductListView.as_view(), name="product-list"),
    path("create-product/", views.AddNewProduct.as_view(), name="add-product"),
    path("update/<int:id>/<slug:slug>/", views.UpdateProducts.as_view(), name="update-product"),
    path("delete-product/", views.DeleteProduct.as_view(), name="delete-product"),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    
    # Category urls
    # path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path("create-category/", views.CreateCategory.as_view(), name="create-category"),
    path("list-category/", views.ListCategories.as_view(), name="list-category"),
    path("update-category/", views.UpdateCategories.as_view(), name="update-category"),
    path("delete-category/", views.DeleteCategories.as_view(), name="delete-category"),
]
