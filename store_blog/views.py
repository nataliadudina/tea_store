from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from store_blog.models import Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'image')
    extra_context = {'page_title': 'TeaBlog: write', 'title': 'Writing a story'}
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
    extra_context = {'page_title': 'TeaBlog', 'title': 'TeaBlog'}

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(publication=Article.Status.PUBLISHED)


class ArticleDetailView(DetailView):
    model = Article
    extra_context = {'page_title': 'TeaBlog: read'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'image', 'publication')
    extra_context = {'page_title': 'TeaBlog: edit', 'title': 'Updating the story'}
    success_url = reverse_lazy('store_blog:list')

    def get_success_url(self):
        return reverse('store_blog:view', args=[self.object.slug])

    def test_func(self):
        article = self.get_object()
        return self.request.user.groups.filter(name='content-manager').exists() or self.request.user == article.author


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'store_blog/article_delete.html'
    extra_context = {'page_title': 'TeaBlog', 'title': 'Delete the story'}
    success_url = reverse_lazy('store_blog:list')

    def test_func(self):
        article = self.get_object()
        return self.request.user.groups.filter(name='content-manager').exists() or self.request.user == article.author
