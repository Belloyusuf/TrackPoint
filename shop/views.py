from django.shortcuts import render, get_object_or_404
from . models import Product, Category, Shelf, StockHistory
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from . forms import ProductForm
from cart.forms import CartAddProductForm
from sweetify.views import SweetifySuccessMixin
from django.db.models import Count, Sum
import sweetify
import requests






# Create Categories
class CreateCategory(SweetifySuccessMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'content/create_category.html'
    success_message = 'Category Created'
    success_url = reverse_lazy('product_app:create-category')


# List Categories
class ListCategories(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "content/category_list.html"

    def get_queryset(self):
        """Return all categories with total product on each."""
        return Category.objects.annotate(total_products=Count("products"))
    

# Update Categories
class UpdateCategories(SweetifySuccessMixin, UpdateView):
    model = Category
    template_name = 'content/update_category'
    success_message = 'Category updated successfully'
    success_url = 'product_app:update_category'


# Delete Categories
class DeleteCategories(SweetifySuccessMixin, DeleteView):
    model = Category
    template_name = 'content/delete_category'
    success_message = 'Category deleted successfully'
    success_url = reverse_lazy('product_app:dashboard')


# Create Shelf
class ShelfCreateView(SweetifySuccessMixin, CreateView):
    model = Shelf
    fields = "__all__"
    success_message = "Shelf Created"
    success_url = reverse_lazy('product_app:create-shelf')
    template_name = "content/shelf_create.html"


# Update Shelf
class ShelfUpdateView(SweetifySuccessMixin, UpdateView):
    model = Shelf
    fields = "__all__"
    success_message = "Shelf Update"
    success_url = reverse_lazy('product_app:update-shelf')
    template_name = "content/shelf_update.html"


# List Shelves
class ShelfListView(SweetifySuccessMixin, ListView):
    model = Shelf
    context_object_name = 'shelves'
    template_name = "content/shelf_create.html"

    def get_queryset(self):
        """Return all shelf with total product on each."""
        return Category.objects.annotate(total_products=Count("products"))


# Create Product
class AddNewProduct(SweetifySuccessMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'content/create_product.html'
    success_message = 'Product Added Successfully'
    success_url = reverse_lazy('product_app:add-product')


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



# List Available Products
class ProductListView(ListView):
    model = Product
    template_name = 'content/product_list.html'
    context_object_name = 'products'
    
    


# Product Details
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm(product=product)  # Pass product to form

    return render(request, 'content/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })



class UpdateProducts(SweetifySuccessMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'content/update_product.html'
    success_message = 'Product Updated Successfully'

    def get_success_url(self):
        # After the object is saved, we can safely access self.object
        return reverse_lazy('product_app:update-product', args=[self.object.id, self.object.slug])


# Delete Products
class DeleteProduct(SweetifySuccessMixin, DeleteView):
    model = Product
    template_name = 'content/delete_product.html'
    success_message = 'Product Deleted Successfully'
    success_url = 'product_app:dashboard'




def product_stock_history(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_history = StockHistory.objects.filter(product=product).order_by('-timestamp')

    return render(request, 'content/stock_history.html', {
        'product': product,
        'stock_history': stock_history
    })