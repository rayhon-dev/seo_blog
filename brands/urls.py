from . import views
from django.urls import path


app_name = 'brands'

urlpatterns = [
    path('create/', views.create_brand, name='create')
]