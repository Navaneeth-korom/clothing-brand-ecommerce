from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
    ]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "city"
    ]
