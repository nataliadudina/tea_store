from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.CharField(max_length=100, unique=True, db_index=True)
    content = models.TextField(blank=True, null=True, db_index=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/blog/', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    publication = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PUBLISHED,
    )
    views_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'

