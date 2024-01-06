from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, TeaProduct, Version
from .templatetags.main_tags import get_random_products
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ProductForm, VersionForm
from django.forms import inlineformset_factory


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

    return render(request, 'main/contact.html', {'title': 'Contact Tea Shop'})


# def catalog(request):
#     return render(request, 'main/catalog.html')

class CatalogListView(ListView):
    model = TeaProduct
    template_name = 'main/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['object_list']

        for product in products:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version

        return context


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

        product = context['object']   # Get product object
        active_version = Version.objects.filter(product=product, is_active=True).first()    # Get product active version
        context['active_version'] = active_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = TeaProduct
    form_class = ProductForm
    template_name = 'main/product_form.html'
    extra_context = {'title': 'Adding a new product'}

    def get_success_url(self):
        type_slug = self.object.category.slug
        item_slug = self.object.slug
        return reverse('product', kwargs={'type_slug': type_slug, 'item_slug': item_slug})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(TeaProduct, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST)
        else:
            context_data['formset'] = version_formset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        self.object = form.save(commit=False)    # without saving the data to a database
        self.object.author = self.request.user   # assign the current user as author
        
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = TeaProduct
    form_class = ProductForm
    template_name = 'main/product_form.html'
    extra_context = {'title': 'Editing product information'}

    def get_success_url(self):
        type_slug = self.object.category.slug
        item_slug = self.object.slug
        return reverse('product', kwargs={'type_slug': type_slug, 'item_slug': item_slug})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(TeaProduct, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)

        # Adds version and active version into the context
        context_data['versions'] = Version.objects.filter(product=self.object)
        context_data['active_version'] = Version.objects.filter(product=self.object, is_active=True)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            active_instances = [instance for instance in instances if instance.is_active]
            if len(active_instances) > 1:
                formset._non_form_errors = forms.ValidationError('Only one active version allowed.')
                return self.form_invalid(form)
            for instance in instances:
                instance.product = self.object
                instance.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = TeaProduct
    template_name = 'main/product_confirm_delete.html'

    def get_success_url(self):
        type_slug = self.object.category.slug    # Get type_slug
        return reverse('types', kwargs={'type_slug': type_slug})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')
