from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("my_posts/", views.MyPosts.as_view(), name="my_posts"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    # path("", views.blog_list, name="blog_list"), # function based view
    path("about/", views.about, name="about"),
    path("create_post/", views.PostCreateView.as_view(), name="create_post"),
    path("update_post/<int:pk>", views.PostUpdateView.as_view(), name="update_post"),
    path("delete_post/<int:pk>", views.PostDeleteView.as_view(), name="delete_post"),
]
