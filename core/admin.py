from django.contrib import admin
from .models import (
    WebsiteCategory, WebsitePackage, PackageFeature, Project,
    ProjectScreenshot, QuoteRequest, QuoteRequestFeature, ContactMessage,
)


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1


@admin.register(WebsiteCategory)
class WebsiteCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(WebsitePackage)
class WebsitePackageAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "min_price", "max_price", "is_active", "sort_order")
    list_filter = ("category", "is_active")
    list_editable = ("min_price", "max_price", "is_active", "sort_order")
    search_fields = ("name", "short_description")
    inlines = [PackageFeatureInline]


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_published", "created_at")
    list_filter = ("category", "is_featured", "is_published")
    list_editable = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "technologies")
    inlines = [ProjectScreenshotInline]


class QuoteRequestFeatureInline(admin.TabularInline):
    model = QuoteRequestFeature
    extra = 0
    can_delete = False
    readonly_fields = ("feature_name", "price_at_quote")


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "package", "tier", "estimated_total", "status", "created_at")
    list_filter = ("status", "tier", "package", "created_at")
    list_editable = ("status",)
    search_fields = ("name", "email", "phone", "company")
    readonly_fields = ("base_price", "additional_total", "estimated_total", "created_at")
    inlines = [QuoteRequestFeatureInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
