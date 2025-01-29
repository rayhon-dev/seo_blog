from django.db import models
from django.utils.text import slugify
from products.base_model import BaseModel


class Catalog(BaseModel):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Catalog, self).save(*args, **kwargs)

