from django.db import models
from django.urls import reverse
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}    # Dictionary containing parameters for nullable fields


class StockManager(models.Manager):
    """Custom model manager for filtering products in stock"""
    def in_stock(self):
        return self.get_queryset().filter(in_stock=TeaProduct.Status.IN_STOCK)


class TeaProduct(models.Model):

    class Status(models.TextChoices):
        """Enum representing the possible statuses of a product"""
        IN_STOCK = 'in_stock', 'In Stock'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'

    name = models.CharField(max_length=100, verbose_name='Title')
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    description = models.TextField(**NULLABLE)
    ingredients = models.CharField(max_length=255, **NULLABLE)
    flavour = models.CharField(max_length=255, **NULLABLE)
    aroma = models.CharField(max_length=255, **NULLABLE)
    preparation = models.CharField(max_length=255, **NULLABLE)
    preview = models.ImageField(upload_to='images/tea/', **NULLABLE, verbose_name='Image path')
    price = models.DecimalField(decimal_places=2, max_digits=8)
    category = models.ForeignKey('TeaCategory', on_delete=models.PROTECT, related_name='cat')

    in_stock = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_STOCK,
    )
    time_created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)

    objects = models.Manager()    # Default manager for this model
    stock_objects = StockManager()    # Custom manager for filtering products in stock

    def save(self, *args, **kwargs):
        """Generates slug from model's name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # calls save method of the parent class to save the changes to the db

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def get_absolute_url(self):
        return reverse('product', kwargs={'type_slug': self.category.slug, 'item_slug': self.slug})


class TeaCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.TextField(**NULLABLE)
    image = models.ImageField(upload_to='images/types/', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('types', kwargs={'type_slug': self.slug})


class Version(models.Model):
    product = models.ForeignKey(TeaProduct, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=10)
    version_name = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    is_active = models.BooleanField(default=False, verbose_name='active version')

    def __str__(self):
        return f"{self.product} - Version {self.version_name}"

    class Meta:
        verbose_name = 'version'
        verbose_name_plural = 'versions'
        # Ensures that there can only be one active version per product
        unique_together = (('product', 'version_number'),)
