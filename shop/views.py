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

    # def get_queryset(self):
    #     """Return all categories with total product on each."""
    #     return Category.objects.annotate(total_products=Count("products"))
    

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
    success_url = reverse_lazy('product_app:shelf-create')
    template_name = "content/shelf_create.html"

    # Check if shelf exist
    def form_valid(self, form):
        if Shelf.objects.filter(name=form.cleaned_data.get("name")).exists():
            sweetify.error(self.request, "Shelf already exists")
            return self.form_valid(form)
        return super().form_valid(form)


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
    template_name = "content/shelf_list.html"

    # def get_queryset(self):
    #     """Return all shelf with total product on each."""
    #     return Category.objects.annotate(total_products=Count("products"))


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


# Low Stock List
def low_stock_products(request):
    """
    Display products with low stock but not out of stock.
    """
    LOW_STOCK_THRESHOLD = 100  # Define your threshold for low stock

    low_stock_products = Product.objects.filter(
        quantity_in_stock__lte=LOW_STOCK_THRESHOLD, quantity_in_stock__gt=0  # Excludes out-of-stock
    )
    total_revenue = low_stock_products.aggregate(total_revenue=Sum("selling_price"))["total_revenue"] or 0

    return render(
        request,
        "content/low_stock_products.html",
        {"products": low_stock_products, "total_revenue": total_revenue},
    )



# Out of Stock List
def out_of_stock_products(request):
    """
    Display products that are out of stock.
    """
    out_of_stock_products = Product.objects.filter(quantity_in_stock__lte=0)
    return render(request, 'content/out_of_stock_products.html', {'products': out_of_stock_products})



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