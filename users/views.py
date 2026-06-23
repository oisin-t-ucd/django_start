from pprint import pprint

# Create your views here.
from django.contrib import messages  # import for messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required #Added import here

from .forms import UserRegisterForm

#
#

# 6. Create a register view in views.py and to use the form
# users/views.py


def register(request):
    if request.method == "POST":
        print("request.POST:")
        print(request.POST)
        form = UserRegisterForm(request.POST)  # ERROR 1 is here
        if form.is_valid():
            print("FORM IS VALID")
            form.save()
            print("FORM CLEANED DATA:")
            pprint(form.data)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
        else:
            print("FORM IS NOT VALID")
            print("FORM ERRORS:")
            pprint(form.errors)
            print("FORM DATA:")
            pprint(form.data)
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})  # ERROR 3 is here


@login_required # Added decorator here
def profile(request):
    return render(request, "users/profile.html")
