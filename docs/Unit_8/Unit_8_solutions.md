# Django Profiles & Architecture: Exercise Solutions

This document contains the solutions for the User Profiles and Media Handling practical exercises. Review the code snippets and explanations to verify your work and understand the underlying architectural concepts.

---

## Exercise 1: Taming the Uploads (Image Optimization)

To prevent users from uploading massive files that drain server resources, we intercept the image processing right after it hits the file system using the `Pillow` library.

**`users/models.py`**

```python
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the built-in save method
    def save(self, *args, **kwargs):
        # 1. Run the default save method first to safely store the file
        super().save(*args, **kwargs) 

        # 2. Open the newly saved image using Pillow
        img = Image.open(self.image.path) 

        # 3. Check if the image exceeds our target dimensions
        if img.height > 150 or img.width > 150:
            # 4. Define the maximum allowed dimensions
            output_size = (150, 150)
            
            # 5. Resize the image (this maintains the aspect ratio)
            img.thumbnail(output_size)
            
            # 6. Overwrite the original large file with the optimized version
            img.save(self.image.path)

```

---

## Exercise 2: The N+1 Hunt (Database Efficiency)

This is a classic backend engineering problem. Here is how to fix the query efficiency and write a test directly in your view to see exactly how many database queries Django is running behind the scenes.

**`users/views.py`**

```python
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import connection, reset_queries

def user_directory(request):
    # reset_queries() clears the query log so we only count this specific view
    reset_queries() 
    
    # ---------------------------------------------------------
    # THE BAD WAY (Commented Out): The N+1 Problem
    # ---------------------------------------------------------
    # users = list(User.objects.all()) 
    # for u in users:
    #     # Forcing the DB hit for every single user
    #     _ = u.profile.image.url 
    
    # ---------------------------------------------------------
    # THE GOOD WAY: Performing the SQL JOIN
    # ---------------------------------------------------------
    users = list(User.objects.select_related('profile').all())
    for u in users:
        # Django already fetched this, so it doesn't hit the DB again
        _ = u.profile.image.url 

    # Print the exact number of queries made to your terminal
    print(f"Total database queries run: {len(connection.queries)}")
    
    return render(request, 'users/user_directory.html', {'users': users})

```

*Note: For `connection.queries` to log data, your `DEBUG` setting in `settings.py` must be set to `True`.*

**`users/templates/users/user_directory.html`**

```html
{% extends "blog/base.html" %}
{% block content %}
    <h1>Community Directory</h1>
    <div class="user-list">
        {% for user in users %}
            <div class="media mb-3">
                <img class="rounded-circle account-img" src="{{ user.profile.image.url }}" alt="{{ user.username }}">
                <div class="media-body">
                    <h4>{{ user.username }}</h4>
                    <p>{{ user.email }}</p>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock content %}

```

---

## Exercise 3: The Explicit Refactor (Architectural Trade-offs)

Signals can hide the flow of execution. Here is how we remove the "magic" and create the profile explicitly inside the registration view.

**1. Disable the Signal (`users/apps.py`)**

```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Comment this out or delete it entirely to disable the signal
    # def ready(self):
    #     import users.signals

```

**2. Update the View (`users/views.py`)**

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile # Don't forget to import your Profile model!

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save() returns the newly created User instance
            new_user = form.save()
            
            # Explicitly create the profile tied to this new user
            Profile.objects.create(user=new_user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

```

---

## Exercise 4: Graceful Fallbacks (Template Logic)

If the database relation is severed or a file goes missing, we don't want our front-end to break. Django templates silently suppress `RelatedObjectDoesNotExist` errors, making it easy to check if the profile and image exist.

**`users/templates/users/profile.html` (or any template displaying the image)**

```html
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <div class="media">
        
        {% if user.profile.image %}
            <img class="rounded-circle account-img" src="{{ user.profile.image.url }}" alt="Profile Picture">
        {% else %}
            <img class="rounded-circle account-img" src="/media/default.jpg" alt="Default Profile Picture">
        {% endif %}
        
        <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
        </div>
    </div>
    
    </div>
{% endblock content %}

```