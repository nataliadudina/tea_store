from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from store_blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'image', 'publication')
    success_url = reverse_lazy('store_blog:list')

    def form_valid(self, form):
        if form.is_valid:
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
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

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(publication=Article.Status.PUBLISHED)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'image',)
    success_url = reverse_lazy('store_blog:list')

    def form_valid(self, form):
        if form.is_valid:
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

            image = form.cleaned_data['image']
            if image:
                new_article.image = image
                new_article.save()

            return super().form_valid(form)

    def get_success_url(self):
        return reverse('store_blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'store_blog/article_delete.html'
    success_url = reverse_lazy('store_blog:list')

