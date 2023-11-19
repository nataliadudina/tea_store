from django.contrib import admin, messages
from main.models import TeaProduct, TeaCategory


@admin.register(TeaCategory)
class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_display_links = ('name',)
    ordering = ['name']
    list_filter = ('name',)
    search_fields = ('pk', 'name',)


@admin.register(TeaProduct)
class TeaProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category', 'in_stock',)
    list_display_links = ('name',)
    list_editable = ('price', 'in_stock',)
    list_filter = ('name', 'category',)
    ordering = ['category__name', 'price']
    list_per_page = 10
    search_fields = ('name', 'category__name',)    # includes search by category name
    list_select_related = ('category',)  # pre-loads related categories
    actions = ['set_status_in_stock', 'set_status_out_of_stock']


    @admin.action(description='Set "in stock" status')
    def set_status_in_stock(self, request, queryset):
        count = queryset.update(in_stock=TeaProduct.Status.IN_STOCK)
        self.message_user(request, f'The status of {count} items set to "in stock".')

    @admin.action(description='Set "out of stock" status')
    def set_status_out_of_stock(self, request, queryset):
        count = queryset.update(in_stock=TeaProduct.Status.OUT_OF_STOCK)
        self.message_user(request, f'The status of {count} items set to "out of stock".', messages.WARNING)

