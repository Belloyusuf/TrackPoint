from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('create-order/', views.order_create, name='create-order'),
    path('invoice/<int:order_id>/', views.order_invoice, name='invoice'),
]
