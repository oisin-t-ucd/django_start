from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    # If we want to use a basic template view we don't need to add a view class in views.py:
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
]
