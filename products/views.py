from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def product_list(request):
    """ A view to return the index page """

    return render(request, 'products/product-list.html')


def about(request):
    """ A view to return the about page """

    return render(request, 'products/about.html')