from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('create/', views.create_product, name='create'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail, name='detail'),
    path('category/<slug:category>/', views.product_by_category, name='category'),
    path('list/', views.product_by_category, name='list'),
]
