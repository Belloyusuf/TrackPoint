from django.urls import path
from . import views



app_name = 'product_app'


urlpatterns = [
    # Product urls
    path("products-list", views.ProductListView.as_view(), name="product-list"),
    path("create-product/", views.AddNewProduct.as_view(), name="add-product"),
    path("update/<int:id>/<slug:slug>/", views.UpdateProducts.as_view(), name="update-product"),
    path("delete-product//<int:id>/<slug:slug>/", views.DeleteProduct.as_view(), name="delete-product"),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    
    # Category urls
    # path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path("create-category/", views.CreateCategory.as_view(), name="create-category"),
    path("list-category/", views.ListCategories.as_view(), name="list-category"),
    path("update-category/", views.UpdateCategories.as_view(), name="update-category"),
    path("delete-category/", views.DeleteCategories.as_view(), name="delete-category"),

    # Stock History
    path('product/<int:product_id>/stock-history/', views.product_stock_history, name='product-stock-history'),

    # Shelves url
    path("shelfs-list/", views.ShelfListView.as_view(), name="shelves"),
    path("shelfs-create/", views.ShelfCreateView.as_view(), name="shelf-create"),
    path("shelfs-update/<int:pk>/", views.ShelfUpdateView.as_view(), name="shelf-update"),

    # Stock Levels
    path('low-stock/', views.low_stock_products, name='low-stock-products'),
    path('out-of-stock/', views.out_of_stock_products, name='out-of-stock-products'),
    
    # Stock Adjustment
    path('adjustment-list/', views.list_product_for_adjustment, name='adjust_stock'),
    path('adjust-product/<int:product_id>/', views.adjust_stock, name='adjust_stock_product'),
    path('stock-adjustment-history/', views.stock_adjustment_history, name='adjust_history'),

]
