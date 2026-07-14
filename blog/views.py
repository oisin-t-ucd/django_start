from django.contrib.auth.mixins import (  # Import UserPassesTestMixin here
    LoginRequiredMixin,
)
from django.db import connection, reset_queries
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .mixins import AuthorRequiredMixin
from .models import Post


# Class Based Blog list view:
class PostListView(ListView):
    # model = Post
    queryset = Post.objects.filter(status=1, is_deleted=False)
    # use this if you want to use a template with a name other than 'blog/post_list.html'
    # template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html Changed here.
    # context_object_name = 'posts' #Updated here. Now the default name is set equal to 'posts'
    ordering = [
        "-created_on"
    ]  # Change here the - will order the posts from newest to oldest.

    def get_queryset(self):
        # 1. Fetch the default queryset (which includes the ordering from above)
        qs = super().get_queryset()

        # 2. Check if there is a 'q' parameter in the URL (e.g., /?q=django)
        query = self.request.GET.get("q")

        # 3. If a query exists, filter the queryset
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))

        return qs


class MyPosts(ListView):

    template_name = "blog/my_posts.html"  # <app>/<model>_<viewtype>.html Changed here.

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_on")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create a Post"
        context["submit_button_text"] = "Create Post"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update a Post"
        context["submit_button_text"] = "Update Post"
        return context


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    fields = ["title", "content"]
    success_url = reverse_lazy(
        "users:profile"
    )  # Here we are redirecting the user back to the homepage after deleting a Post successfully

    def delete(self, request, *args, **kwargs):
        # 1. Grab the specific post object
        self.object = self.get_object()

        # 2. Toggle the boolean flag instead of deleting from the database
        self.object.is_deleted = True
        self.object.save()

        # 3. Redirect the user to the success URL
        return HttpResponseRedirect(self.get_success_url())


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
    post = Post.objects.get(id=1)
    redirect(post)
    print(f"AFTER RENDER QUERIES: {len(connection.queries)}")
    # if len(connection.queries):
    #     pprint(connection.queries)

    return res


# @permission_required("blog.add_post", raise_exception=True)
# def create_post(request):
#     return render(request, "blog/create_post.html")
