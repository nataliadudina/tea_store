from django.urls import path
from .views import ProductDetailView, CatalogListView, CategoryListView, IndexView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, ContactView
from . import views
from django.views.decorators.cache import cache_page

# Example of URLs when Function Based Views (FBVs) are used
# urlpatterns = [
#     path('', views.index, name='home'),
#     path('contact/', views.contact, name='contact'),
#     path('catalog/', views.catalog, name='catalog'),
#     path('catalog/<slug:type_slug>/', views.category, name='types'),
#     path('catalog/<slug:type_slug>/<slug:item_slug>/', views.product, name='product'),
# ]

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),  # all product types
    path('catalog/<slug:type_slug>/', CategoryListView.as_view(), name='types'),  # one product type
    path('catalog/<slug:type_slug>/<slug:item_slug>/', cache_page(60)(ProductDetailView.as_view()), name='product'),  # product page
    path('new/', ProductCreateView.as_view(), name='product_form'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_edit'),
    path('<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # footer links (empty pages with stubs)
    path('tea-history/', cache_page(60*60)(views.tea_history), name='tea-history'),
    path('shipping-and-handling/', cache_page(60*60)(views.shipping), name='shipping'),
    path('returns-and-exchanges/', cache_page(60*60)(views.returns), name='returns'),
    path('contacts/', cache_page(60*60)(views.contacts), name='contacts'),
]
