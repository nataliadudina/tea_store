"""Создайте сервисную функцию, которая будет отвечать за выборку категорий
и которую можно переиспользовать в любом месте системы.
Добавьте низкоуровневое кеширование для списка категорий.
 Нужно создать функцию, которая будет получать список категорий из кэша, если кэш включен.

Класть список в кэш если кэш включен и списка в кэше нет.

Если кэш выключен - делать запрос в ОРМ.

def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['кладем данные по ключу'] = cache_category() - используем написанную нами функцию, которая проверяет наличие кэша, если он есть , отдает из кэша данные, если нет, то идет в бд и отдает данные оттуда
        return context_data
        """

from django.core.cache import cache
from django.conf import settings
from .models import TeaCategory


def get_categories():
    if settings.CACHE_ENABLED:
        # Trying to get categories from the cache
        categories = cache.get('tea_categories')
        if categories is not None:
            return categories

    # If caching is disabled or categories are not found in the cache, the selection is performed
    categories = TeaCategory.objects.all()

    if settings.CACHE_ENABLED:
        # Saving categories in the cache for a specified time (1 hour)
        cache.set('tea_categories', categories, timeout=3600)

    return categories
