from django.db import models
from products.base_model import BaseModel


class Color(BaseModel):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name
