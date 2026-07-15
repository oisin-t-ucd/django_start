from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("security_settings/", views.security_settings, name="security_settings"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
    path("delete_account/", views.delete_account, name="delete-account"),
    path("user/<str:username>/", views.public_profile, name="public-profile"),
]
