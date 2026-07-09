---

# Django User Authentication: Exercise Solutions

This document contains the solutions for the User Authentication practical exercises. Review the code snippets and explanations to verify your work.

---

## Exercise 1: The Dynamic Dashboard (Template Logic)

To create a page that dynamically changes based on session state, we intentionally **do not** use the `@login_required` decorator on the view. The view must be accessible to everyone so the template can handle the logic.

**1. Create the View (`users/views.py`)**

```python
from django.shortcuts import render

def dashboard(request):
    return render(request, 'users/dashboard.html')

```

**2. Map the URL (`django_project/urls.py`)**

```python
from users import views as user_views

urlpatterns = [
    # ... other paths ...
    path('dashboard/', user_views.dashboard, name='dashboard'),
]

```

**3. Implement the Template Logic (`users/templates/users/dashboard.html`)**

```html
{% extends "blog/base.html" %}
{% block content %}
    <div class="content-section">
        {% if user.is_authenticated %}
            <h2>Welcome to your Dashboard, {{ user.username }}!</h2>
            <p>Here is your recent activity:</p>
            <table class="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Action</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Today</td>
                        <td>Account Login</td>
                        <td><span class="text-success">Success</span></td>
                    </tr>
                </tbody>
            </table>
        {% else %}
            <h2>Welcome to our platform!</h2>
            <p>Sign up today to access premium features and view your personal dashboard.</p>
            <a class="btn btn-primary" href="{% url 'register' %}">Sign Up Now</a>
            <a class="btn btn-outline-info" href="{% url 'login' %}">Login</a>
        {% endif %}
    </div>
{% endblock content %}

```

---

## Exercise 2: The `?next=` Parameter Maze (Routing & Decorators)

This exercise reinforces how Django protects routes and handles intended destinations.

**1. Create the Protected View (`users/views.py`)**

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def security_settings(request):
    return render(request, 'users/security.html')

```

**2. Map the URL (`django_project/urls.py`)**

```python
urlpatterns = [
    # ... other paths ...
    path('security/', user_views.security_settings, name='security'),
]

```

**3. Verify Settings (`django_project/settings.py`)**
Ensure this line is at the bottom of your settings file so Django knows where to redirect unauthenticated users:

```python
LOGIN_URL = 'login'

```

**How it works:** When a logged-out user hits `/security/`, the `@login_required` decorator intercepts the request. It redirects to `/login/` but appends `?next=/security/`. Upon successful login, Django's `LoginView` reads the `next` parameter and honors the original request.

---

## Exercise 3: User Feedback with Messages

Because `LoginView` and `LogoutView` are built-in class-based views, we can't easily inject `messages.success()` like we did in our custom `register` function. The cleanest solution is to subclass these views in your `users/views.py` file.

**1. Subclass the Auth Views (`users/views.py`)**

```python
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Use SuccessMessageMixin for the Login view
class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = "Welcome back, %(username)s!"

# Override the dispatch method for the Logout view
class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been securely logged out.")
        return super().dispatch(request, *args, **kwargs)

```

**2. Update URLs to Use Custom Views (`django_project/urls.py`)**
Replace the default `auth_views` with your new custom views:

```python
from users import views as user_views

urlpatterns = [
    # ... other paths ...
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout'),
]

```

---

## Exercise 4: Password Change View (Stretch Goal)

Implementing the password change feature requires using two built-in views: one for the form, and one for the success confirmation.

**1. Import and Map the URLs (`django_project/urls.py`)**

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... other paths ...
    
    # The form to change the password
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), 
         name='password_change'),
         
    # The success page after changing the password
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
         name='password_change_done'),
]

```

**2. Create the Form Template (`users/templates/users/password_change.html`)**

```html
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Change Password</legend>
                {{ form|crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Update Password</button>
            </div>
        </form>
    </div>
{% endblock content %}

```

**3. Create the Success Template (`users/templates/users/password_change_done.html`)**

```html
{% extends "blog/base.html" %}
{% block content %}
    <div class="content-section">
        <h2>Password Updated Successfully</h2>
        <div class="alert alert-success">
            Your password has been changed. 
        </div>
        <a href="{% url 'profile' %}" class="btn btn-outline-info">Return to Profile</a>
    </div>
{% endblock content %}

```

**4. Update the Navbar (`blog/templates/blog/base.html`)**

```html
{% if user.is_authenticated %}
    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
    <a class="nav-item nav-link" href="{% url 'password_change' %}">Change Password</a>
    <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
{% else %}
    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
    <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
{% endif %}

```