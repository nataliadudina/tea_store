from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, TeaProduct
from .templatetags.main_tags import get_random_products
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views import View
from .forms import ProductForm


import json


# def index(request):
#
#     slides = [
#         {
#             'img': 'main/images/slide1.jpg',
#             'alt': 'quiet contemplation',
#             'text': '"There is something in the nature <br>of tea that leads us into a world <br>of quiet contemplation of life." <br>- Lin Yutang.',
#             'text_color': 'black'
#         },
#         {
#             'img': 'main/images/slide2.jpg',
#             'alt': 'wisdom in every sip',
#             'text': '"Tea is the perfect blend of warmth, comfort, <br>and wisdom in every sip." <br>- Arthur Wing Pinero',
#             'text_color': 'white'
#         },
#         {
#             'img': 'main/images/slide3.jpg',
#             'alt': 'warming inside',
#             'text': '"A cup of tea is like a gentle hug for the soul, <br>warming you from the inside out." <br>- Aaron Fisher',
#             'text_color': 'white'
#         },
#     ]
#
#     random_products = get_random_products()
#     context = {
#         'slides': slides,
#         'random_products': random_products
#     }
#     # return render(request, 'main/index.html', {'random_products': random_products})
#     return render(request, 'main/index.html', context)


class IndexView(View):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        slides = [
            {
                'img': 'main/images/slide1.jpg',
                'alt': 'quiet contemplation',
                'text': '"There is something in the nature <br>of tea that leads us into a world <br>of quiet contemplation of life." <br>- Lin Yutang.',
                'text_color': 'black'
            },
            {
                'img': 'main/images/slide2.jpg',
                'alt': 'wisdom in every sip',
                'text': '"Tea is the perfect blend of warmth, comfort, <br>and wisdom in every sip." <br>- Arthur Wing Pinero',
                'text_color': 'white'
            },
            {
                'img': 'main/images/slide3.jpg',
                'alt': 'warming inside',
                'text': '"A cup of tea is like a gentle hug for the soul, <br>warming you from the inside out." <br>- Aaron Fisher',
                'text_color': 'white'
            },
        ]

        random_products = get_random_products()
        context = {
            'slides': slides,
            'random_products': random_products
        }

        return render(request, self.template_name, context)


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


# def catalog(request):
#     return render(request, 'main/catalog.html')

class CatalogListView(ListView):
    model = TeaProduct
    template_name = 'main/catalog.html'


# def category(request, type_slug):
#     tea_type = get_object_or_404(TeaCategory, slug=type_slug)   # gets an object from the db or raises Http404
#
#     # QuerySet of products in stock of the specified category
#     in_stock_products = TeaProduct.stock_objects.filter(category=tea_type, in_stock=TeaProduct.Status.IN_STOCK)
#     data = {'category': tea_type, 'in_stock': in_stock_products}
#     return render(request, 'main/category.html', data)

class CategoryListView(ListView):
    template_name = 'main/category.html'
    context_object_name = 'in_stock'

    def get_category(self):
        # Gets TeaCategory object by slug from URL
        return get_object_or_404(TeaCategory, slug=self.kwargs['type_slug'])

    def get_queryset(self):
        # Returns QuerySet of products in stock of the specified category
        return TeaProduct.stock_objects.filter(category=self.get_category(), in_stock=TeaProduct.Status.IN_STOCK)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


# def product(request, type_slug, item_slug):
#     cat = get_object_or_404(TeaCategory, slug=type_slug)
#     prod = get_object_or_404(TeaProduct, slug=item_slug, category=cat)
#     return render(request, 'main/product.html', {'category': cat, 'product': prod})

class ProductDetailView(DetailView):
    model = TeaProduct
    template_name = 'main/product.html'
    context_object_name = 'product'    # TeaProduct object
    slug_url_kwarg = 'item_slug'    # <slug:item_slug> => self.kwargs['item_slug']

    def get_object(self, queryset=None):
        type_slug = self.kwargs.get('type_slug')
        item_slug = self.kwargs.get('item_slug')
        cat = get_object_or_404(TeaCategory, slug=type_slug)
        prod = get_object_or_404(TeaProduct, slug=item_slug, category=cat)
        return prod

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_slug = self.kwargs.get('type_slug')
        cat = get_object_or_404(TeaCategory, slug=type_slug)
        context['category'] = cat
        return context


class ProductCreateView(CreateView):
    model = TeaProduct
    form_class = TeaProductForm
    template_name = 'main/product_create.html'
    success_url = reverse_lazy('main:product')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')
