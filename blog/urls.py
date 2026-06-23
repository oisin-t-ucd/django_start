from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("about/", views.about, name="about"),
    path("create_post/", views.create_post, name="create_post"),
]
