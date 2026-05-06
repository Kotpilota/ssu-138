from django.contrib import admin
from .models import Lead, LeadNote


class LeadNoteInline(admin.TabularInline):
    model = LeadNote
    extra = 0
    readonly_fields = ("author", "created_at")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "object_type", "status", "email_sent", "telegram_sent", "created_at")
    list_filter = ("status", "object_type", "email_sent", "telegram_sent")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at", "updated_at", "ip", "user_agent", "email_sent", "telegram_sent")
    inlines = [LeadNoteInline]
    date_hierarchy = "created_at"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
