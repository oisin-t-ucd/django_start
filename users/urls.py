from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "users"
urlpatterns = [
    path("security_settings/", views.security_settings, name="security_settings"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html", success_url=reverse_lazy("home")
        ),
        name="password_change",
    ),
    path(
        "logout/",
        views.CustomLogoutView.as_view(),
        name="logout",
    ),
]
