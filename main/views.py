from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, TeaProduct
from .templatetags.main_tags import get_random_products


import json


def index(request):
    random_products = get_random_products()
    return render(request, 'main/index.html', {'random_products': random_products})


def contact(request):

    # receives POST-request
    if request.method == 'POST':
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        phone = request.POST.get('phone', ' ')
        message = request.POST.get('message', ' ')

        user_data = {
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Message': message
        }

        # saves data to users_data.json
        with open('users_data.json', 'a', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False)
            f.write('\n')

    return render(request, 'main/contact.html')


def catalog(request):
    return render(request, 'main/catalog.html')


def category(request, type_slug):
    tea_type = get_object_or_404(TeaCategory, slug=type_slug)   # gets an object from the db or raises Http404

    # QuerySet of products in stock of the specified category
    in_stock_products = TeaProduct.stock_objects.filter(category=tea_type, in_stock=TeaProduct.Status.IN_STOCK)
    data = {'category': tea_type, 'in_stock': in_stock_products}
    return render(request, 'main/category.html', data)


def product(request, type_slug, item_slug):
    cat = get_object_or_404(TeaCategory, slug=type_slug)
    prod = get_object_or_404(TeaProduct, slug=item_slug, category=cat)
    return render(request, 'main/product.html', {'category': cat, 'product': prod})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')
