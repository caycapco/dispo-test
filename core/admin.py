from django.contrib import admin
from .models import UserProfile, Facility, Message
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
    list_display = ("email", "firstName", "lastName", "is_staff",)
    list_filter = ("email", "firstName", "lastName", "is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "firstName", "lastName", "password","is_superuser")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "firstName", "lastName", "password", "is_staff", "is_superuser")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)



# Register your models here.
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Facility)
admin.site.register(Message)