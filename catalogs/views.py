from django.shortcuts import render, redirect
from .models import Catalog



def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')


        if category_name and description:
            Catalog.objects.create(
                category_name=category_name,
                description=description,
            )
            return redirect('home')

    return render(request, 'catalogs/category-create.html')
