# Guide: Setting Up Cloudinary with Django

This guide will walk you through integrating **Cloudinary** into your Django project for handling user-uploaded media files. Cloudinary is an excellent choice for student projects because it provides a generous free tier and automatically handles image resizing and optimization.

## Prerequisites

1. A Django project already set up.
2. A free [Cloudinary account](https://cloudinary.com/).
3. Your **API Environment variable** (This is a single string starting with `cloudinary://...` found right on your Cloudinary Dashboard in "Settings" > "API Keys").

---

## Step 1: Install Dependencies

You will need the `cloudinary` SDK and the `django-cloudinary-storage` package, which integrates Cloudinary with Django's `FileField` system.

Run the following command in your terminal:

```bash
pip install cloudinary django-cloudinary-storage

```

---

## Step 2: Configure `settings.py`

When you use the `CLOUDINARY_URL` environment variable, the Cloudinary SDK automatically detects your credentials. You don't need to write out your API keys in your settings file!

1. Add `cloudinary_storage` and `cloudinary` to your `INSTALLED_APPS`. Order matters here:

```python
INSTALLED_APPS = [
    # ... your other apps ...
    'django.contrib.staticfiles', 
    # ensure these are below staticfiles:
    'cloudinary_storage',
    'cloudinary',
    # ...
]

```

2. Tell Django to use Cloudinary for media files:

```python
# settings.py

# Set Cloudinary as the default storage for media files (this is also shown in the render deploy doc)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
}

```

**Crucial Note on Environment Variables:** For this to work, you **must** have `CLOUDINARY_URL` set in your environment variables.

* **Locally:** Put `CLOUDINARY_URL=cloudinary://your-api-key:your-api-secret@your-cloud-name` in your `.env` file (using a package like `python-decouple` or `django-environ` to load it).
* **On Render (Production):** Add `CLOUDINARY_URL` and its value directly into the "Environment Variables" section of your Render Web Service dashboard.

---

## Step 3: Use it in your Models

You can now use `ImageField` or `FileField` in your models just as you would with local storage.

```python
from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    # The file will automatically be uploaded directly to Cloudinary
    avatar = models.ImageField(upload_to='avatars/')

```

---

## Step 4: Handle Media in Development vs. Production

### In `settings.py`:

Ensure your static files (CSS/JS) are handled by standard Django (or WhiteNoise in production) while keeping your media files directed to Cloudinary.

```python
# Static files (CSS, JS) - typically handled by WhiteNoise in production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files - handled by Cloudinary
MEDIA_URL = '/media/'

```

### In `urls.py`:

Because the files live on Cloudinary's servers, you typically do **not** need to add the standard `+ static(settings.MEDIA_URL, ...)` routing to your main `urls.py` file. The database will naturally save and serve the full Cloudinary URL.

---

## Summary of the Data Flow

1. **User uploads a file** through your Django `Form` or `ModelForm`.
2. **Django `FileField**` automatically detects the `CLOUDINARY_URL` environment variable and sends the file to Cloudinary.
3. **Cloudinary** stores the file and returns a unique, secure URL.
4. **Django** saves that URL text into your database (Neon/Postgres).
5. **Browser** fetches the file directly from the Cloudinary CDN when the page loads, keeping your Render server fast and free from heavy media downloads.