from django.contrib import admin
from . models import Product, Category, Shelf


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'quantity_in_stock', 'selling_price', 'expiry_date')
    search_fields = ('name', 'barcode')
    list_filter = ('category', 'expiry_date')
