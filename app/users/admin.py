from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_active", "created_at")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("phone", "stripe_customer_id", "created_at", "updated_at")},
        ),
    )

    readonly_fields = ("created_at", "updated_at")
