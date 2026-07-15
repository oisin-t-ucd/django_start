# Student Guide: Setting Up Django-Allauth (Modern Layouts/Elements) with Django 5.2 and Crispy Forms

When building your web development projects, handling registration, login, and password resets securely is essential. Instead of writing authentication logic from scratch, we use **`django-allauth`**, the industry standard.

Modern versions of `django-allauth` use a streamlined template architecture called **Layouts and Elements**. Instead of overriding dozens of separate HTML templates (like `login.html`, `signup.html`, etc.), we can style our *entire* authentication system by modifying just **one base layout** and **two reusable UI elements**.

---

## The Big Picture: How Template Overrides Work

By default, Django finds and renders the default templates packed inside the installed `django-allauth` package. If we want to change how they look, we:

1. Recreate the specific folder structure inside our project's global `templates/` folder.
2. Download or copy only the specific template files we want to change from the [Official Allauth Template Repository](https://codeberg.org/allauth/django-allauth/src/branch/main/allauth/templates).
3. **Delete any template we didn't modify.** If Django doesn't find a file locally, it safely falls back to the package default. This keeps your codebase lean, clean, and easy to maintain.

---

## Step 1: Install the Packages

Run this command in your project's active virtual environment to install the required libraries:

```bash
pip install django-allauth django-crispy-forms crispy-bootstrap5

```

---

## Step 2: Configure `settings.py`

Open your project's `settings.py` and update the following configuration blocks.

### 1. `INSTALLED_APPS`

Add the core `allauth` applications, `crispy_forms`, and the Bootstrap 5 crispy template pack.

```python
INSTALLED_APPS = [
    # Default Django Apps...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-Party Apps
    "crispy_forms",
    "crispy_bootstrap5",

    "allauth",
    "allauth.account",
]

```

### 2. `MIDDLEWARE`

Add the `allauth` account middleware. **Order matters:** Always place it below `AuthenticationMiddleware`.

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Allauth Middleware
    "allauth.account.middleware.AccountMiddleware",
]

```

### 3. Templates, Backends & Crispy Settings

Add these parameters to point Django to your local `templates` directory, configure the authenticators, and tell Crispy to use Bootstrap 5:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"], # Points to your root templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Required by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# See this page for more allauth options: https://docs.allauth.org/en/latest/common/configuration.html
# Allauth Behavior Configurations
# the asterisk makes a field required here
# add/remove email/username as desired
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

# add/remove email/username as desired, must align with the above setting:
ACCOUNT_LOGIN_METHODS = {"email"}

```

---

## Step 3: Setup Routing (`urls.py`)

Include the automatic authentication paths in your project's main `urls.py` file:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # Handles login, signup, password resets, etc.
]

```

---

## Step 4: Create & Override the Templates

Now we hook up our global project styles and integrate `crispy-forms` directly into the `allauth` layout architecture.

### 1. Structure Your Directories

Set up your global templates folder exactly like this:

```text
your_project/
│
├── templates/
│   ├── base.html                 # Your main project layout (navbar, footer, etc.)
│   └── allauth/
│       ├── layouts/
│       │   └── base.html         # Overrides Allauth's base layout wrapper
│       └── elements/
│           ├── fields.html        # Overrides how form fields render
│           └── button.html       # Overrides how buttons render

```

### 2. Prepare Your Project-Wide `templates/base.html`

Ensure your main layout has a clean container and a clear `block body` where content can inject itself:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block head_title %}Project Title{% endblock %}</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    
    <!-- Site-wide Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">My App</a>
        </div>
    </nav>

    <!-- Main Page Content Grid -->
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                {% block body %}
                <!-- Allauth wrappers inject their views here -->
                {% endblock %}
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 Bundle JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

```

### 3. Override `templates/allauth/layouts/base.html`

Instead of allowing `allauth` to generate a separate unstyled page, we force its base layout to extend from our master `base.html`.

```html
{% extends "base.html" %}
{% load i18n %}

{% block body %}
<div class="card shadow-sm p-4 mt-4">
    <!-- Displays allauth system message alerts cleanly using Bootstrap styling -->
    {% if messages %}
        <div class="messages mb-3">
            {% for message in messages %}
                <div class="alert alert-info py-2">{{ message }}</div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Injects the current authentication view (e.g., login form or signup form) -->
    {% block content %}
    {% endblock content %}
</div>
{% endblock body %}

```

---

## Step 5: Route Elements Through Crispy Forms

We do not need to manually apply `|crispy` filters inside individual login or signup templates anymore. By overriding `allauth` UI elements globally, *every* authentication input automatically styles itself.

### 1. Customize the Form Field Element (`templates/allauth/elements/fields.html`)

Open `fields.html` and replace its contents with this single snippet:

```html
{% load crispy_forms_tags %}
{{ attrs.form|crispy }}

```

### 2. Customize the Button Element (`templates/allauth/elements/button.html`)

To style all submitting elements uniformly:

```html
<!-- Distinguish form submission buttons from secondary interaction links -->
{% if attrs.type == "submit" %}
    <button class="btn btn-primary w-100 mt-3" type="submit">
        {% slot %}{% endslot %}
    </button>
{% else %}
    <button class="btn btn-outline-secondary btn-sm" type="{{ attrs.type }}">
        {% slot %}{% endslot %}
    </button>
{% endif %}

```

---

## Step 6: Verify and Clean Up

Once your custom `allauth/layouts/base.html`, `allauth/elements/fields.html`, and `allauth/elements/button.html` are created:

1. **Delete all other downloaded folders** (such as `account/` or other unused files in `elements/`) from your local project's `templates/allauth/` directory.
2. `django-allauth` will instantly fall back to its internal copies for all non-modified files, which are now seamlessly fed through your custom layouts and crispy elements!

---

## Step 7: Run Your App

1. **Run Database Migrations** to build the tables required by Allauth and Django authentication:
```bash
python manage.py migrate

```


2. **Start your local development server**:
```bash
python manage.py runserver

```


3. **Test Your Custom Pages** in your web browser:
* Sign In: `[http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)`
* Sign Up: `[http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/)`