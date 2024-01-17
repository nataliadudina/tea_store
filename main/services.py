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
