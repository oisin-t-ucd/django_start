# Django Profile Update & CRUD: Exercise Solutions

Welcome to the solutions guide! Remember, there are many ways to solve a problem in programming. If your code looks a bit different but still achieves the correct result, that's perfectly fine. Use these solutions to check your work and understand the core Django concepts.

---

## Exercise 1: The "Bio" Expansion (Custom Validation)

### 1. Update `models.py`
First, we add the `bio` field to the `Profile` model and run `python manage.py makemigrations` and `python manage.py migrate`.


```python
# users/models.py
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=False) # Added bio field

    def __str__(self):
        return f'{self.user.username} Profile'
        
    # ... save method remains the same ...

```

### 2. Update `forms.py`

Next, we add `bio` to the `fields` list and write our custom `clean_bio` method.

```python
# users/forms.py
from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image', 'bio'] # Added bio to fields

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        
        # Check if bio exists before running string methods
        if bio:
            # 1. Check for forbidden word
            forbidden_word = "spam"
            if forbidden_word in bio.lower():
                raise ValidationError("Please keep your bio professional. Remove forbidden words.")
            
            # 2. Check word count
            word_count = len(bio.split())
            if word_count > 50:
                raise ValidationError(f"Bio is too long! (Current: {word_count} words. Max: 50)")
                
        return bio

```

---

## Exercise 2: The Standalone Contact Form (Standard Forms)

### 1. Create the Form in `forms.py`

Notice we use `forms.Form` here, not `forms.ModelForm`.

```python
# users/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

```

### 2. Handle the Form in `views.py`

```python
# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Print the cleaned data dictionary to the terminal
            print("Received Contact Data:", form.cleaned_data)
            
            # Flash success message and redirect (PRG Pattern)
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact') # Assuming 'contact' is the url name
    else:
        form = ContactForm()
        
    return render(request, 'users/contact.html', {'form': form})

```

---

## Exercise 3: The Public Profile (CRUD - Read Operation)

### 1. Update `urls.py`

Add the dynamic route that accepts a string as the username.

```python
# users/urls.py (or your main urls.py)
from django.urls import path
from . import views

urlpatterns = [
    # ... other paths ...
    path('user/<str:username>/', views.public_profile, name='public-profile'),
]

```

### 2. Create the View in `views.py`

Use `get_object_or_404` to handle non-existent users gracefully.

```python
# users/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def public_profile(request, username):
    # This will automatically throw a 404 page if the user doesn't exist
    viewed_user = get_object_or_404(User, username=username)
    
    context = {
        'viewed_user': viewed_user
    }
    return render(request, 'users/public_profile.html', context)

```

*(You would then create a `public_profile.html` template that displays `{{ viewed_user.username }}`, `{{ viewed_user.profile.image.url }}`, and `{{ viewed_user.profile.bio }}`.)*

---

## Exercise 4: The "Danger Zone" (CRUD - Delete Operation)

### 1. Create the Delete View

This handles the confirmation page and the actual deletion logic.

```python
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Grab the user object
        user = request.user
        
        # IMPORTANT: Log the user out BEFORE deleting them to clear the session cookie
        logout(request)
        
        # Delete the user (this cascades and deletes their profile too)
        user.delete()
        
        messages.info(request, "Your account has been successfully deleted. We're sorry to see you go!")
        return redirect('blog-home') # Redirect to home page
        
    # If GET request, render the confirmation page
    return render(request, 'users/delete_confirm.html')

```

### 2. Create the Confirmation Template (`delete_confirm.html`)

```html
{% extends "blog/base.html" %}
{% block content %}
    <div class="content-section">
        <h2>Are you sure you want to delete your account?</h2>
        <p class="text-danger">This action cannot be undone. All your data will be lost.</p>
        
        <form method="POST">
            {% csrf_token %}
            <button class="btn btn-danger" type="submit">Yes, Delete My Account</button>
            <a class="btn btn-secondary" href="{% url 'profile' %}">Cancel</a>
        </form>
    </div>
{% endblock content %}

```

---

## Exercise 5: The Bouncer: File Size Validation

### 1. Update `ProfileUpdateForm` in `forms.py`

We add a `clean_image` method to validate the file size before it ever gets saved to the database or processed by the `save()` method.

```python
# users/forms.py
from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image', 'bio']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        # Check if an image was actually uploaded
        if image:
            # size is measured in bytes. 
            # 2MB = 2 * 1024 * 1024 bytes (2,097,152 bytes)
            max_size = 2 * 1024 * 1024 
            
            if image.size > max_size:
                raise ValidationError("File too large. Size should not exceed 2MB.")
                
        return image

```
