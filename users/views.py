from pprint import pprint
from django.contrib.auth.models import User

# Create your views here.
from django.contrib import messages  # import for messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required  # Added import here
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


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
    return render(request, "users/profile.html")


def dashboard(request):
    return render(request, "users/dashboard.html")


@login_required
def security_settings(request):
    return render(request, "users/security_settings.html")


def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})