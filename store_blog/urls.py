from django.urls import path
from .views import ArticleCreateView, BlogListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from store_blog.apps import StoreBlogConfig

app_name = StoreBlogConfig.name

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),  # list of articles
    path('read/<int:pk>/', ArticleDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'),
]
