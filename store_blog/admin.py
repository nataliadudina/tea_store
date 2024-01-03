from django.contrib import admin

from store_blog.models import Article


@admin.register(Article)
class TeaCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    ordering = ['title']
    list_filter = ('title',)
    search_fields = ('pk', 'title',)
    save_on_top = True
