
# authentication url 

from django.urls import path, include
from . import views



app_name = "authentication_app"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),  # default django authentications
    path('accounts/login/', views.login_view, name='login'),
    path("update-admin/<int:pk>/", views.UpdateAdmin.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteAdmin.as_view(), name="delete"),
    path('register/', views.register, name='register'),
    path('profile/', views.edit_profile, name="edit"),

 
]
