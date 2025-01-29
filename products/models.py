from django.db import models
from django.utils.text import slugify
from catalogs.models import Catalog
from brands.models import Brand
from colors.models import Color
from django.urls import reverse
from .base_model import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='products')
    colors = models.ManyToManyField(Color, related_name='products')
    desc = models.TextField()
    image = models.ImageField(upload_to='product_images/', default='default_image.jpg')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Product, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse(
            'products:detail',
            kwargs={
                'year': self.created_at.year,
                'month': self.created_at.month,
                'day': self.created_at.day,
                'slug': self.slug
            })


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rating = models.PositiveIntegerField()
    content = models.TextField(null=True)


    def __str__(self):
        return f'Review for {self.product.name} by {self.name}'

    class Meta:
        ordering = ['-created_at']