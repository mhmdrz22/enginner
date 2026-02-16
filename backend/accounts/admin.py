from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdminConfig(UserAdmin):
    """Custom User Admin configuration without username field."""
    
    model = User
    
    # Search and filtering
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_verified", "created_date")
    ordering = ("-created_date",)
    
    # List display (removed username)
    list_display = (
        "email",
        "get_full_name_display",
        "is_active",
        "is_staff",
        "is_verified",
        "created_date"
    )
    
    # Fieldsets for viewing/editing existing users
    fieldsets = (
        (_("Authentication"), {
            "fields": ("email", "password")
        }),
        (_("Personal Info"), {
            "fields": ("first_name", "last_name")
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_verified"
            )
        }),
        (_("Group Permissions"), {
            "fields": (
                "groups",
                "user_permissions",
            )
        }),
        (_("Important Dates"), {
            "fields": (
                "last_login",
                "last_login_date",
                "created_date",
                "updated_date"
            )
        }),
    )
    
    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_verified"
            ),
        }),
    )
    
    # Read-only fields
    readonly_fields = (
        "last_login",
        "last_login_date",
        "created_date",
        "updated_date"
    )
    
    def get_full_name_display(self, obj):
        """Display full name in list view."""
        return obj.get_full_name()
    get_full_name_display.short_description = _("Full Name")
    

admin.site.register(User, UserAdminConfig)
