from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from .models import Post


# Create your views here.
def blog_list(request):
    """A view to return the index page"""
    posts = Post.objects.all()
    recent_posts = posts.order_by("-created_on")[:5]
    custom_message = "Welcome to my blog!"
    return render(
        request,
        "blog/blog-list.html",
        {
            "posts": posts,
            "custom_message": custom_message,
            "recent_posts": recent_posts,
        },
    )


def about(request):
    """A view to return the about page"""

    return render(request, "blog/about.html")



@permission_required('blog.add_post', raise_exception=True)
def create_post(request):
    return render(request, 'blog/create_post.html')