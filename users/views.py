from pprint import pprint

# Create your views here.
from django.contrib import messages  # import for messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required  # Added import here
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection, reset_queries
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


class CustomLoginView(SuccessMessageMixin, auth_views.LoginView):
    success_message = "Successfully logged in!"

    template_name = "users/login.html"


class CustomLogoutView(auth_views.LogoutView):
    template_name = "users/logout.html"

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been securely logged out.")
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == "POST":
        print("request.POST:")
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID")
            form.save()
            print("FORM CLEANED DATA:")
            pprint(form.data)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("users:login")
        else:
            print("FORM IS NOT VALID")
            print("FORM ERRORS:")
            pprint(form.errors)
            print("FORM DATA:")
            pprint(form.data)
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(data=request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            data=request.POST, files=request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated")
            return redirect("users:profile")  # Changes here

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "users/profile.html", context)


def dashboard(request):
    reset_queries()
    users = User.objects.select_related("profile").all()

    print(f"BEFORE RENDER QUERIES: {len(connection.queries)}")
    print(f"users:{len(users)}")
    res = render(request, "users/dashboard.html", {"users": users})
    print(f"AFTER RENDER QUERIES: {len(connection.queries)}")
    if len(connection.queries):
        pprint(connection.queries)
    return res


@login_required
def security_settings(request):
    return render(request, "users/security_settings.html")


def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})
