from django.shortcuts import render
from . models import Product, Category, Shelf
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy




# Create your views here.


def dashboard(request):
    products = Product.objects.all()
    return render(request, 'content/dashboard.html', {'products': products})


# Create Categories
class CreateCategory(CreateView, SuccessMessageMixin):
    model = Category
    fields = ['name']
    template_name = 'content/create_category.html'
    success_message = 'Category Addedd'
    success_url = reverse_lazy('product_app:create-category')


# List Categories
class ListCategories(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'content/category_list.html'
    

# Update Categories
class UpdateCategories(UpdateView, SuccessMessageMixin):
    model = Category
    template_name = 'content/update_category'
    success_message = 'Category updated successfully'
    success_url = 'product_app:update_category'


# Delete Categories
class DeleteCategories(DeleteView, SuccessMessageMixin):
    model = Category
    template_name = 'content/delete_category'
    success_message = 'Category deleted successfully'
    success_url = 'product_app:dashboard'


# Create Product
class AddNewProduct(CreateView, SuccessMessageMixin):
    model = Product
    fields = '__all__'
    template_name = 'content/create_product.html'
    success_message = 'Product Added Successfully'
    success_url = reverse_lazy('product_app:dashboard')



# List Available Products
class ListProducts(ListView, SuccessMessageMixin):
    model = Product
    template_name = 'content/product_list.html'
    context_object_name = 'products'    


# Update Products
class UpdateProducts(UpdateView, SuccessMessageMixin):
    model = Product
    template_name = 'content/update_product.html'
    success_message = 'Product Updated Successfully'
    success_url = 'product_app:update_product'
    

# Delete Products
class DeleteProduct(DeleteView, SuccessMessageMixin):
    model = Product
    template_name = 'content/delete_product.html'
    success_message = 'Product Deleted Successfully'
    success_url = 'product_app:dashboard'