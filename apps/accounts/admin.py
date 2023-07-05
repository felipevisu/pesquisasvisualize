from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from .models import User
from .forms import UserAdminCreationForm

class UserAdmin(BaseUserAdmin):
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Informações Pessoais', {'fields': ['first_name', 'last_name']}),
        ('Tipo', {
            'fields': ['client', 'user_type']
        }),
        ('Permissões', {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
        }),
        ('Informações extras', {'fields': readonly_fields}),
    )
    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'first_name', 'last_name', 'client', 'user_type', 'password1', 'password2'],
        }),
    )
    list_display = ['username', 'first_name', 'last_name', 'client', 'user_type']


admin.site.register(User, UserAdmin)
admin.site.register(Permission)