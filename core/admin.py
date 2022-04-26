from django.contrib import admin

from .models import Profile


class BaseClassAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Profile, BaseClassAdmin)
