from django.shortcuts import render

# Create your views here.
def blog_list(request):
    """ A view to return the index page """

    return render(request, 'blog-list.html')


def about(request):
    """ A view to return the about page """

    return render(request, 'about.html')