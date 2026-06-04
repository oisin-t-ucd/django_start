from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product


# Create your views here.
def product_list(request):
    """A view to return the index page"""
    return render(
        request,
        "products/product-list.html",  # {"products": Product.objects.all()}
    )


def about(request):
    """A view to return the about page"""

    return render(request, "products/about.html")
