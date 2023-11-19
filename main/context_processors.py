from .models import TeaCategory

"""
Context processor - a function that takes a query object 
and returns a dictionary with the context
"""


def tea_categories(request):
    categories = TeaCategory.objects.all()
    return {'tea_categories': categories}
