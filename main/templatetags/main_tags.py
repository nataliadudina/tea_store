from django import template
from main.models import TeaProduct


register = template.Library()


@register.simple_tag(name='random_items')
def get_random_products():
    return TeaProduct.stock_objects.filter(in_stock=TeaProduct.Status.IN_STOCK).order_by('?')[:4]


@register.filter()
def mediapath(image_path):
    if image_path:
        return f'/media/{image_path}'
    return '/media/images/types/default_cat.png'


@register.simple_tag()
def imagepath_tag(image_field):
    if image_field:
        return image_field.url
    return '/media/images/tea/default_tea.jpg'
