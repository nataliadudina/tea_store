from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import TeaCategory, TeaProduct, Version
from .templatetags.main_tags import get_random_products
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from .forms import ProductForm, VersionForm,  ContactForm
from django.forms import inlineformset_factory

import json


class IndexView(View):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        slides = [
            {
                'img': 'main/images/slide1.jpg',
                'alt': 'quiet contemplation',
                'text': '"There is something in the nature <br>of tea that leads us into a world <br>'
                        'of quiet contemplation of life." <br>- Lin Yutang.',
                'text_color': 'black'
            },
            {
                'img': 'main/images/slide2.jpg',
                'alt': 'wisdom in every sip',
                'text': '"Tea is the perfect blend of warmth, comfort, <br>and wisdom in every sip." <br>'
                        '- Arthur Wing Pinero',
                'text_color': 'white'
            },
            {
                'img': 'main/images/slide3.jpg',
                'alt': 'warming inside',
                'text': '"A cup of tea is like a gentle hug for the soul, <br>warming you from the inside out." <br>'
                        '- Aaron Fisher',
                'text_color': 'white'
            },
        ]

        random_products = get_random_products()  # Retrieves four random products
        # Context dictionary passed to the template
        context = {
            'slides': slides,
            'random_products': random_products
        }

        return render(request, self.template_name, context)


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('home')
    extra_context = {'page_title': 'Contact us', 'title': 'Contact Tea Shop'}

    def form_valid(self, form):
        user_data = form.cleaned_data

        # Loads existing data from the file (if any)
        try:
            with open('users_data.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []

        # Appends new user's data to the existing data
        existing_data.append(user_data)

        # Writes the entire list back to the file
        with open('users_data.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return super().form_valid(form)


# FBV for catalog_list_view
# def catalog(request):
#     products = TeaProduct.objects.all()
#     for product in products:
#         active_version = Version.objects.filter(product=product, is_active=True).first()
#         product.active_version = active_version
#         context = {
#             'products': products,
#         }
#         return render(request, 'main/catalog.html', context)


class CatalogListView(ListView):
    """
       A class-based view that lists all the tea types.

       This view fetches all the tea types from the database and passes them to the template.
       Additionally, it adds the active version of each product to the context.
       """
    model = TeaProduct
    template_name = 'main/catalog.html'
    extra_context = {'page_title': 'TeaShop: Catalog'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['object_list']

        for prod in products:
            active_version = Version.objects.filter(product=prod, is_active=True).first()
            prod.active_version = active_version

        return context


# FBV for category_list_view
# def category(request, type_slug):
#     cat = get_object_or_404(TeaCategory, slug=type_slug)  # gets an object from the db or raises Http404
#     products = TeaProduct.stock_objects.filter(category=cat, in_stock=TeaProduct.Status.IN_STOCK)
#     for product in products:
#         active_version = Version.objects.filter(product=product, is_active=True).first()
#         product.active_version = active_version
#     context = {
#         'category': cat,
#         'in_stock': products,
#     }
#     return render(request, 'main/category.html', context)


class CategoryListView(ListView):
    """ View for listing tea products within a specific category"""
    template_name = 'main/category.html'
    context_object_name = 'in_stock'

    def get_category(self):
        # Gets TeaCategory object associated with the current request
        return get_object_or_404(TeaCategory, slug=self.kwargs['type_slug'])

    # Returns QuerySet of products in stock for the current category
    def get_queryset(self):
        return TeaProduct.stock_objects.filter(category=self.get_category(), in_stock=TeaProduct.Status.IN_STOCK)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        context['page_title'] = f"TeaShop: {context['category'].name}"
        return context


# FBV for product_detail_view
# def product(request, type_slug, item_slug):
#     cat = get_object_or_404(TeaCategory, slug=type_slug)
#     prod = get_object_or_404(TeaProduct, slug=item_slug, category=cat)
#     active_version = Version.objects.filter(product=prod, is_active=True).first()
#     context = {
#          'product': prod,
#          'category': cat,
#          'active_version': active_version,
#      }
#     return render(request, 'main/product.html', context)


class ProductDetailView(DetailView):
    """
    View for showing details of a single tea product.
    Fetches the product by both slugs from the URL, adds the active version of the product
    to the context, and renders the template with the context.
      """

    model = TeaProduct
    template_name = 'main/product.html'
    context_object_name = 'product'  # TeaProduct object
    slug_url_kwarg = 'item_slug'  # <slug:item_slug> —> self.kwargs['item_slug']

    # Override the get_object method to get the product by both slugs
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

        product = context['object']
        active_version = Version.objects.filter(product=product, is_active=True).first()  # Get product active version
        context['active_version'] = active_version
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = TeaProduct
    form_class = ProductForm
    template_name = 'main/product_form.html'
    extra_context = {'title': 'Adding a new product'}
    permission_required = 'main.add_teaproduct'

    def get_success_url(self):
        type_slug = self.object.category.slug
        item_slug = self.object.slug
        return reverse('product', kwargs={'type_slug': type_slug, 'item_slug': item_slug})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Create a formset for the Version model
        version_formset = inlineformset_factory(TeaProduct, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            # If the request method is POST, initialize the formset with the POST data
            context_data['formset'] = version_formset(self.request.POST)
        else:
            # Otherwise, initialize the formset without any data
            context_data['formset'] = version_formset()
        return context_data

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        # Get the formset from the context data
        formset = self.get_context_data()['formset']
        self.object = form.save()

        # If the formset is valid, save it to the database along with the product
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = TeaProduct
    form_class = ProductForm
    template_name = 'main/product_form.html'
    extra_context = {'title': 'Editing product information'}
    permission_required = 'main.change_teaproduct'

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

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if formset.is_valid():
            instances = formset.save(commit=False)

            # Check if there is more than one active version, which is not allowed
            active_instances = [instance for instance in instances if instance.is_active]
            if len(active_instances) > 1:
                # Add a non-form error if multiple active versions
                formset._non_form_errors = forms.ValidationError('Only one active version allowed.')
                return self.form_invalid(form)

            # Save each instance and associate it with the current product
            for instance in instances:
                instance.product = self.object
                instance.save()
            return super().form_valid(form)
        else:
            # If the formset is not valid, return to the form with errors
            return self.form_invalid(form)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = TeaProduct
    template_name = 'main/product_confirm_delete.html'
    permission_required = 'main.delete_teaproduct'

    def get_success_url(self):
        type_slug = self.object.category.slug  # Get type_slug
        return reverse('types', kwargs={'type_slug': type_slug})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')


def tea_history(request):
    return render(request, 'main/footer/history.html', {'page_title': 'Tea History'})


def shipping(request):
    return render(request, 'main/footer/shipping.html', {'page_title': 'Shipping'})


def returns(request):
    return render(request, 'main/footer/returns.html', {'page_title': 'Returns'})


def contacts(request):
    return render(request, 'main/footer/contacts.html', {'page_title': 'Contacts'})
