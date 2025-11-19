from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    if category_slug:
        # Страница конкретной категории
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
    else:
        # Вкладка "Все" — убираем дубли по имени
        all_products = Product.objects.filter(available=True).order_by('name', 'id')
        seen = set()
        products = []
        for p in all_products:
            if p.name in seen:
                continue
            seen.add(p.name)
            products.append(p)

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    """Страница одного товара"""
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
        },
    )




