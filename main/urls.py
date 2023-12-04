from django.urls import path
from .views import ProductDetailView, CatalogListView, CategoryListView, IndexView
from . import views

# urlpatterns = [
#     path('', views.index, name='home'),  # main page
#     path('contact/', views.contact, name='contact'),  # contact page
#     path('catalog/', views.catalog, name='catalog'),  # all product types
#     path('catalog/<slug:type_slug>/', views.category, name='types'),  # product type
#     path('catalog/<slug:type_slug>/<slug:item_slug>/', views.product, name='product'),  # product page
# ]

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # main page
    path('contact/', views.contact, name='contact'),  # contact page
    path('catalog/', CatalogListView.as_view(), name='catalog'),  # all product types
    path('catalog/<slug:type_slug>/', CategoryListView.as_view(), name='types'),  # product type
    path('catalog/<slug:type_slug>/<slug:item_slug>/', ProductDetailView.as_view(), name='product'),  # product page
]
