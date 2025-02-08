from django.shortcuts import render, get_object_or_404, redirect
from . models import Product, Category, Shelf, StockHistory, StockAdjustment, StockAdjustmentHistory,\
                     StockTransfer
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



# List products for adjustment 
def list_product_for_adjustment(request):
    """
    List available products before adjusting
    """
    products = Product.objects.all()
    return render(request, "content/adjustment_list.html", {"products":products})



# Stock Adjustment 
def adjust_stock(request, product_id):
    """
    Handles stock adjustments for a product.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        adjustment_type = request.POST.get("adjustment_type")
        quantity = int(request.POST.get("quantity", 0))
        reason = request.POST.get("reason", "").strip()

        if quantity <= 0:
            sweetify.error(request, "Quantity must be greater than zero.")
            return redirect("product_app:adjust_stock_product", product_id=product.id)

        # Create adjustment record and apply changes
        adjustment = StockAdjustment.objects.create(
            product=product,
            adjustment_type=adjustment_type,
            quantity=quantity,
            reason=reason
        )
        adjustment.apply_adjustment()

        # Create a history record for the adjustment
        StockAdjustmentHistory.objects.create(
            product=product,
            adjustment_type=adjustment_type,
            quantity=quantity,
            reason=reason,
            adjusted_by=request.user if request.user.is_authenticated else None  # Allow None for anonymous users
        )

        sweetify.success(request, f"Stock successfully adjusted: {adjustment}")
        return redirect("product_app:adjust_stock_product", product_id=product.id)

    return render(request, "content/adjust_stock.html", {"product": product})



# Adjustment History
def stock_adjustment_history(request):
    """
    Displays the history of stock adjustments.
    """
    adjustments = StockAdjustmentHistory.objects.all()

    return render(request, "content/stock_adjustment_history.html", {"adjustments": adjustments})




# Stock Transfer to shelf
def transfer_stock(request, product_id):
    product = Product.objects.get(id=product_id)
    shelves = Shelf.objects.all()  # Assume all shelves are available for transfer

    if request.method == "POST":
        source_shelf_id = request.POST.get("source_shelf")
        destination_shelf_id = request.POST.get("destination_shelf")
        quantity_transferred = int(request.POST.get("quantity_transferred"))
        reason = request.POST.get("reason", "").strip()

        # Get source and destination shelves
        source_shelf = Shelf.objects.get(id=source_shelf_id)
        destination_shelf = Shelf.objects.get(id=destination_shelf_id)

        # Check if there is enough stock in the source shelf
        if source_shelf.products.filter(id=product.id).exists():
            source_product = source_shelf.products.get(id=product.id)

            if source_product.quantity_in_stock < quantity_transferred:
                sweetify.error(request, "Insufficient stock in source shelf.")
                return redirect('product_app:transfer_stock', product_id=product.id)
            
            # Update stock in source and destination shelves
            source_product.quantity_in_stock -= quantity_transferred
            source_product.save()

            # Update or add stock in the destination shelf
            if destination_shelf.products.filter(id=product.id).exists():
                destination_product = destination_shelf.products.get(id=product.id)
                destination_product.quantity_in_stock += quantity_transferred
                destination_product.save()
            else:
                # Create new product entry in destination shelf if not exists
                destination_shelf.products.add(product, through_defaults={'quantity_in_stock': quantity_transferred})

            # Create StockTransfer record
            StockTransfer.objects.create(
                product=product,
                source_shelf=source_shelf,
                destination_shelf=destination_shelf,
                quantity_transferred=quantity_transferred,
                reason=reason,
                # transferred_by=request.user
            )

            sweetify.success(request, f"Successfully transferred {quantity_transferred} of {product.name}.")
            return redirect('product_app:transfer_stock', product_id=product.id)

    return render(request, 'content/transfer_stock.html', {'product': product, 'shelves': shelves})




# Stock to shelf transfer history
def stock_transfer_history(request):
    transfers = StockTransfer.objects.all().order_by('-transfer_date')
    return render(request, 'content/stock_transfer_to_shelf_history.html', {'transfers': transfers})