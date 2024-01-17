from .models import TeaCategory
from .services import get_categories

"""
Context processor - a function that takes a query object 
and returns a dictionary with the context
"""

def tea_categories(request):
    categories = get_categories()
    return {'tea_categories': categories}
