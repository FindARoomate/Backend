from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Waitlist


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    readonly_fields = ('created_at', 'updated_at',)
    model = CustomUser
    list_display = ('email', 'is_staff',
                    'is_active','created_at', 'updated_at')
    list_filter = ('email', 'is_staff', 'is_active',
                   'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('email',
         'password', 'created_at', 'updated_at')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'created_at', 'updated_at')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Waitlist)
