from django.shortcuts import render
from . models import Product, Category, Shelf
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from . forms import ProductForm
from sweetify.views import SweetifySuccessMixin
from django.http import JsonResponse
import sweetify
import requests







def dashboard(request):
    # Get products and balances as before
    products = Product.objects.all()
    balances = Product.get_total_balances()  # Fetch total balances

    # NewsAPI API Key (replace with your actual API key)
    api_key = 'b65d393754a8465eb261fd03b1255b3b'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    # Fetching news from NewsAPI
    # response = requests.get(url)
    # data = response.json()

    # if response.status_code == 200 and 'articles' in data:
    #     # Extracting the top 5 news headlines
    #     headlines = [{'title': article['title'], 'image': article.get('urlToImage', '') , 'url': article['url']} for article in data['articles'][:5]]
    # else:
    #     headlines = []

    # Pass the products and news to the template
    return render(request, 'content/dashboard.html', {
        'products': products,
        'total_cost_price': balances['total_cost_price'], 
        'total_selling_price': balances['total_selling_price'],
        # 'headlines': headlines,
    })





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
    context_object_name = 'categories'
    template_name = 'content/category_list.html'
    

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
    success_url = 'product_app:dashboard'


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
class ListProducts(SweetifySuccessMixin, ListView):
    model = Product
    template_name = 'content/product_list.html'
    context_object_name = 'products'    


# Update Products
class UpdateProducts(SweetifySuccessMixin, UpdateView):
    model = Product
    template_name = 'content/update_product.html'
    success_message = 'Product Updated Successfully'
    success_url = 'product_app:update_product'
    

# Delete Products
class DeleteProduct(SweetifySuccessMixin, DeleteView):
    model = Product
    template_name = 'content/delete_product.html'
    success_message = 'Product Deleted Successfully'
    success_url = 'product_app:dashboard'