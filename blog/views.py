from pprint import pprint

from django.contrib.auth.decorators import permission_required
from django.db import connection, reset_queries
from django.shortcuts import render

from .models import Post


# Create your views here.
def blog_list(request):
    """A view to return the index page"""
    reset_queries()

    # posts = Post.objects.all()
    posts = Post.objects.prefetch_related("comments__author__profile").all()
    # posts = Post.objects.select_related("comments__author__profile").all()
    recent_posts = posts.order_by("-created_on")[:5]
    custom_message = "Welcome to my blog!"
    print(f"BEFORE RENDER QUERIES: {len(connection.queries)}")
    res = render(
        request,
        "blog/blog-list.html",
        {
            "posts": posts,
            "custom_message": custom_message,
            # "recent_posts": recent_posts,
        },
    )
    print(f"AFTER RENDER QUERIES: {len(connection.queries)}")
    # if len(connection.queries):
    #     pprint(connection.queries)

    return res


def about(request):
    """A view to return the about page"""
    reset_queries()

    print(f"BEFORE RENDER QUERIES: {len(connection.queries)}")

    res = render(request, "blog/about.html")
    print(f"AFTER RENDER QUERIES: {len(connection.queries)}")
    if len(connection.queries):
        pprint(connection.queries)

    return res


@permission_required("blog.add_post", raise_exception=True)
def create_post(request):
    return render(request, "blog/create_post.html")
