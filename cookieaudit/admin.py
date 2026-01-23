from django.contrib import admin
from .models import CookieEvent

@admin.register(CookieEvent)
class CookieEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "cookie_name", "user", "client_ip", "path", "method")
    search_fields = ("cookie_name", "user__username", "client_ip", "path", "user_agent", "cookie_value_preview", "value_sha256")
    list_filter = ("cookie_name", "method", "created_at")
    readonly_fields = [f.name for f in CookieEvent._meta.fields]
    ordering = ("-created_at",)
