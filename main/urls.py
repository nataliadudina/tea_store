from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # main page
    path('contact/', views.contact, name='contact'),  # contact page
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:type_slug>/', views.category, name='types'),  # tea type
    # path('catalog/<slug:type_slug>/<int:pk>/', views.tea, name='tea'),   # item page
]
