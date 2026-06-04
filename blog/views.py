from django.shortcuts import render
from .models import Post


# Create your views here.
def blog_list(request):
    """A view to return the index page"""
    posts = Post.objects.all()
    custom_message = "Welcome to my blog!"
    return render(
        request,
        "blog/blog-list.html",
        {"posts": posts, "custom_message": custom_message},
    )


def about(request):
    """A view to return the about page"""

    return render(request, "blog/about.html")
