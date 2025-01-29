from django.urls import path
from . import views


app_name = 'catalogs'

urlpatterns = [
    path('create/', views.create_category, name='create'),
]