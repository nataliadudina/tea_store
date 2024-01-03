from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from store_blog.models import Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'author', 'image', 'publication')
    extra_context = {'title': 'New Article'}
    success_url = reverse_lazy('store_blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save(commit=False)    # without saving the data to a database
            new_article.slug = slugify(new_article.title)
            new_article.author = self.request.user    # assign the current user as author
            new_article.save()

            image = form.cleaned_data['image']
            if image:
                new_article.image = image
                new_article.save()

            return super().form_valid(form)


class BlogListView(ListView):
    model = Article
    template_name = 'store_blog/blog.html'
    context_object_name = 'articles'
    extra_context = {'title': 'Tea Blog'}

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(publication=Article.Status.PUBLISHED)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'author', 'image',)
    extra_context = {'title': 'Edit Article'}
    success_url = reverse_lazy('store_blog:list')

    def get_success_url(self):
        return reverse('store_blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'store_blog/article_delete.html'
    extra_context = {'title': 'Delete Article'}
    success_url = reverse_lazy('store_blog:list')

