# Create your views here.
from django.contrib import messages  # import for messages
from django.shortcuts import redirect, render

from .forms import UserRegisterForm

#
#

# 6. Create a register view in views.py and to use the form


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            print("username:", username)
            messages.success(request, f"Account created for {username}!")
            return redirect("home")
        else:
            from pprint import pprint

            pprint(form.errors)
    else:
        # this block is only executed for GET requests
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})
