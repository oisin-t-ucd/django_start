from pprint import pprint

# Create your views here.
from django.contrib import messages  # import for messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required  # Added import here
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection, reset_queries
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, ProfileUpdateForm, UserRegisterForm, UserUpdateForm


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


# users/views.py


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Print the cleaned data dictionary to the terminal
            print("Received Contact Data:", form.cleaned_data)

            # Flash success message and redirect (PRG Pattern)
            messages.success(
                request, "Thank you for your message! We will get back to you soon."
            )
            return redirect("users:contact")  # Assuming 'contact' is the url name
    else:
        form = ContactForm()

    return render(request, "users/contact.html", {"form": form})


def public_profile(request, username):
    # This will automatically throw a 404 page if the user doesn't exist
    viewed_user = get_object_or_404(User, username=username)

    context = {"viewed_user": viewed_user}
    return render(request, "users/public_profile.html", context)


@login_required
def delete_account(request):
    print("DELETE ACCOUNT")
    if request.method == "POST":
        # Grab the user object
        user = request.user

        # IMPORTANT: Log the user out BEFORE deleting them to clear the session cookie
        logout(request)

        # Delete the user (this cascades and deletes their profile too)
        user.delete()

        messages.info(
            request,
            "Your account has been successfully deleted. We're sorry to see you go!",
        )
        return redirect("home")  # Redirect to home page

    # If GET request, render the confirmation page
    return render(request, "users/delete_confirm.html")
