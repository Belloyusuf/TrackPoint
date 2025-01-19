from django.contrib import admin
from .models import CustomUser


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'phone', 'email']  # Fields to enable search by


admin.site.register(CustomUser, StudentAdmin)
