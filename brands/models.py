from django.db import models
from products.base_model import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    logo = models.ImageField(upload_to='brand_logos/')

    def __str__(self):
        return self.name

