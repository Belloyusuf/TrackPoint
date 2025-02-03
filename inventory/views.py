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
from django.utils import timezone
from django.db.models import Sum, F
from orders.models import Order, OrderItem





def dashboard(request):
    # Get products and balances as before
    products = Product.objects.all()
    balances = Product.get_total_balances()  # Assuming you have a custom method to calculate total balances

    # NewsAPI API Key (replace with your actual API key)
    api_key = 'b65d393754a8465eb261fd03b1255b3b'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    # Fetching news from NewsAPI
    # response = requests.get(url)
    # data = response.json()

    # if response.status_code == 200 and 'articles' in data:
    #     # Extracting the top 5 news headlines
    #     headlines = [{'title': article['title'], 'image': article.get('urlToImage', ''), 'url': article['url']} for article in data['articles'][:5]]
    # else:
    #     headlines = []

    # Get today's date
    today = timezone.now().date()

    ## Filter OrderItems for today and calculate the total sales amount
    total_sales_today = OrderItem.objects.filter(
        order__created__year=today.year,
        order__created__month=today.month,
        order__created__day=today.day
    ).aggregate(
        total_sales=Sum(F('price') * F('quantity'))  # Multiply price by quantity
    )['total_sales'] or 0  # Default to 0 if no orders today

    # Calculate Today's Profit
    total_profit_today = OrderItem.objects.filter(
        order__created__year=today.year,
        order__created__month=today.month,
        order__created__day=today.day
    ).aggregate(
        total_profit=Sum((F('price') - F('product__cost_price')) * F('quantity'))  # Multiply by quantity
    )['total_profit'] or 0  # Default to 0 if no profit today


    # Calculate total cost price (cost_price * quantity_in_stock for each product)
    total_cost_price = sum(product.cost_price * product.quantity_in_stock for product in products)

    # Calculate total selling price (selling_price * quantity_in_stock for each product)
    total_selling_price = sum(product.selling_price * product.quantity_in_stock for product in products)


    # Define target amounts for sales and profit (these can be dynamic or static values)
    target_sales = 100000  # Example target sales for the day
    target_profit = 100000  # Example target profit for the day

    target_cost_balance = 10000000000
    target_selling_balance = 20000000000

    # Calculate progress percentages
    sales_progress_percentage = (total_sales_today / target_sales) * 100 if target_sales else 0
    profit_progress_percentage = (total_profit_today / target_profit) * 100 if target_profit else 0

    # Calculate progress percentages for cost and selling balances
    target_cost_percentage = (total_cost_price / target_cost_balance) * 100 if target_cost_balance else 0
    target_selling_percentage = (total_selling_price / target_selling_balance) * 100 if target_selling_balance else 0

    # Ensure percentages don't exceed 100%
    sales_progress_percentage = min(sales_progress_percentage, 100)
    profit_progress_percentage = min(profit_progress_percentage, 100)

    # Ensure percentages for cost and selling balances don't exceed 100%
    cost_progress_percentage = min(target_cost_percentage, 100)
    sells_progress_percentage = min(target_selling_percentage, 100)


    # Pass the products, balances, sales, profit, and progress data to the template
    return render(request, 'content/dashboard.html', {
        'products': products,
        'total_cost_price': balances['total_cost_price'], 
        'total_selling_price': balances['total_selling_price'],
        # 'headlines': headlines,
        'total_sales_today': total_sales_today,
        'total_profit_today': total_profit_today,
        'total_cost_price': total_cost_price,
        'total_selling_price': total_selling_price,
        'sales_progress_percentage': sales_progress_percentage,
        'profit_progress_percentage': profit_progress_percentage,
        'cost_progress_percentage': cost_progress_percentage,
        'sells_progress_percentage': sells_progress_percentage
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
    

    # def form_valid(self, form):
    #     # Save the product
    #     form.save()
        
    #     # Show a success toast message
    #     sweetify.toast(self.request, self.success_message, icon="success")
        
    #     # Return an empty form to clear the input fields
    #     return self.render_to_response(self.get_context_data(form=self.form_class()))

    # def form_invalid(self, form):
    #     # If the form is invalid, show an error message
    #     error_message = form.errors.get('__all__', ['Something went wrong.'])[0]
    #     sweetify.toast(self.request, error_message, icon="error")
        
    #     # Return the template with the invalid form data
    #     return self.render_to_response(self.get_context_data(form=form))
    



# Inventory List
class InventoryList(ListView):
    """ List Inventory Information """
    model = InventorySetting
    context_object_name = "inventory"
    template_name = "content/inventory_list.html"



# Update Inventory
class InventoryUpdate(SweetifySuccessMixin, UpdateView):
    """ Update your inventory: Name, Address, Email, Logo ETC"""
    model = InventorySetting
    form_class = InventoryForm
    template_name = "content/inventory_update.html"
    success_message = "Inventory Updated Successfully"
    success_url = reverse_lazy("product_app:inventory-update")