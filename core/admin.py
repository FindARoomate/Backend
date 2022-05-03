from django.contrib import admin

from .models import Profile, RoomateRequest, RequestImages


class BaseClassAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Profile, BaseClassAdmin)
admin.site.register(RoomateRequest, BaseClassAdmin)
admin.site.register(RequestImages, BaseClassAdmin)
