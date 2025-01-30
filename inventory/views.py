from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import InventorySetting
from .forms import InventoryForm
from shop.models import Product, Category
from sweetify.views import SweetifySuccessMixin
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView
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






# Inventory Settings
class InventoryCreateView(SweetifySuccessMixin, CreateView):
    """ Sets your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_create.html"
    success_message = "Inventory Created Successfully"
    success_url = reverse_lazy("product_app:inventory-create")



    def get(self, request, *args, **kwargs):
        # Check if the Inventory Information Already Exists
        if InventorySetting.objects.exists():
            inventory_info = InventorySetting.objects.first() # Get the first the first or (only) inventory object
            sweetify.toast(self.request, "Inventory Information already Exists. You can only update it.", icon="error")
            return redirect(reverse_lazy("inventory_app:inventory-update", kwargs={'pk':inventory_info.pk}))
        return super().get(request, *args, **kwargs)
    


    def post(self, request, *args, **kwargs):
        # Check if the Inventory Information Already Exists
        if InventorySetting.objects.exists():
            inventory_info = InventorySetting.objects.first() # Get the first the first or (only) inventory object
            sweetify.toast(self.request, "Inventory Information already Exists. You can only update it.", icon="error")
            return redirect(reverse_lazy("inventory_app:inventory-update", kwargs={'pk':inventory_info.pk}))
        return super().post(request, *args, **kwargs)
    

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
    


# Update Inventory
class InventoryUpdate(SweetifySuccessMixin, CreateView):
    """ Update your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_update.html"
    success_message = "Inventory Updated Successfully"
    success_url = reverse_lazy("product_app:inventory-update")