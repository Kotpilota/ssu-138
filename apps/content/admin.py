from django.contrib import admin

from .models import SiteSettings, Page, Section, SectionItem


class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 0


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0
    show_change_link = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "page", "block_type", "order", "is_visible")
    list_filter = ("page", "block_type", "is_visible")
    inlines = [SectionItemInline]
