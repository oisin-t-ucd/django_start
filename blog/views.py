from pprint import pprint

from django.db import connection, reset_queries
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Post


# Class Based Blog list view:
class PostListView(ListView):
    model = Post
    # use this if you want to use a template with a name other than 'blog/post_list.html'
    # template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html Changed here.
    # context_object_name = 'posts' #Updated here. Now the default name is set equal to 'posts'
    ordering = [
        "-created_on"
    ]  # Change here the - will order the posts from newest to oldest.


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content"]


# Function Based Blog list view:
def blog_list(request):
    """A view to return the index page"""
    reset_queries()

    # posts = Post.objects.all().order_by("-created_on")
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


# @permission_required("blog.add_post", raise_exception=True)
# def create_post(request):
#     return render(request, "blog/create_post.html")
