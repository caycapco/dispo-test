from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
    list_display = ('email', 'fullname','is_staff',)
    list_filter = ('email', 'fullname','is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'fullname','password','is_superuser')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



# Register your models here.
admin.site.register(UserProfile, CustomUserAdmin)