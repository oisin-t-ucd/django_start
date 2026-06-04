from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='blog_list'),
    path('about/', views.about, name='about'),
]