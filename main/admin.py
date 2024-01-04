from django.contrib import admin, messages
from main.models import TeaProduct, TeaCategory, Version
from django.utils.safestring import mark_safe


@admin.register(TeaCategory)
class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ['name']
    list_filter = ('name',)
    search_fields = ('pk', 'name',)
    save_on_top = True


@admin.register(TeaProduct)
class TeaProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'preview', 'show_preview', 'ingredients', 'flavour', 'aroma', 'preparation', 'price', 'category', 'in_stock']
    list_display = ('name', 'show_preview', 'price', 'category', 'in_stock',)
    list_display_links = ('name',)
    list_editable = ('price', 'in_stock',)
    readonly_fields = ('show_preview',)
    list_filter = ('name', 'category',)
    ordering = ['category__name', 'price']
    list_per_page = 10
    search_fields = ('name', 'description', 'category__name',)    # includes search by category name
    list_select_related = ('category',)  # pre-loads related categories
    actions = ['set_status_in_stock', 'set_status_out_of_stock']
    save_on_top = True

    @admin.display(description='Preview')
    def show_preview(self, item: TeaProduct):
        return mark_safe(f"<img src='{item.preview.url}' width=50")

    @admin.action(description='Set "in stock" status')
    def set_status_in_stock(self, request, queryset):
        count = queryset.update(in_stock=TeaProduct.Status.IN_STOCK)
        self.message_user(request, f'The status of {count} items set to "in stock".')

    @admin.action(description='Set "out of stock" status')
    def set_status_out_of_stock(self, request, queryset):
        count = queryset.update(in_stock=TeaProduct.Status.OUT_OF_STOCK)
        self.message_user(request, f'The status of {count} items set to "out of stock".', messages.WARNING)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'text', 'is_active')
    list_filter = ('product', 'version_name',)
    list_display_links = ('version_name',)
    list_editable = ('is_active',)
