from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review
from catalogs.models import Catalog
from brands.models import Brand
from colors.models import Color


def home(request):
    products = Product.objects.all()

    ctx = {
        'products': products,
    }
    return render(request, 'index.html', ctx)
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        colors = request.POST.getlist('color')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')

        if name and price and brand and category and colors and desc and image:
            product = Product.objects.create(
                name=name,
                price=price,
                brand=Brand.objects.get(id=brand),
                category=Catalog.objects.get(id=category),
                desc=desc,
                image=image
            )
            colors = Color.objects.filter(id__in=colors)
            product.colors.set(colors)

            return redirect('home')

    categories = Catalog.objects.all()
    brands = Brand.objects.all()

    colors = Color.objects.all()

    ctx = {
        'categories': categories,
        'brands': brands,
        'colors': colors,
    }

    return render(request, 'products/product-create.html', ctx)


def product_detail(request, year, month, day, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )

    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        content = request.POST.get('content')


        Review.objects.create(
            product=product,
            name=name,
            email=email,
            rating=rating,
            content=content,
        )
        return redirect('products:detail', year=product.created_at.year, month=product.created_at.month,
                        day=product.created_at.day, slug=product.slug)
    for review in reviews:
        review.full_stars = [i for i in range(review.rating)]
        review.empty_stars = [i for i in range(5 - review.rating)]

    ctx = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product-detail.html', ctx)


def product_by_category(request):
    products = Product.objects.all()
    catalogs = Catalog.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    category_id = request.GET.get('category')
    brands_id = request.GET.getlist('brand')
    colors_id = request.GET.getlist('color')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_brands = None
    selected_colors = None

    if category_id:
        products = products.filter(category_id__in=category_id)

    if brands_id:
        products = products.filter(brand__id__in=brands_id)
        selected_brands = brands.filter(id__in=brands_id)
        brands = brands.exclude(id__in=brands_id)

    if colors_id:
        products = products.filter(colors__id__in=colors_id)
        selected_colors = colors.filter(id__in=colors_id)
        colors = colors.exclude(id__in=colors_id)



    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)



    ctx = {
        'products': products,
        'catalogs': catalogs,
        'brands': brands,
        'colors': colors,
        'min_price': min_price,
        'max_price': max_price,
        'selected_brands': selected_brands,
        'selected_colors': selected_colors
    }

    return render(request, 'products/product-by-category.html', ctx)
