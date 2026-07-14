#  Deploying Your Real-Time Django Inbox on Render (Free Tier)

This guide is a direct follow-up to the **Real-Time Django Inbox with SSE** tutorial. Getting an asynchronous application to run on a production server requires a few adjustments to your project, especially when using a highly constrained environment like Render's Free Tier.

Because Server-Sent Events (SSE) keep connections open indefinitely, a standard synchronous WSGI server (like Gunicorn) will freeze. We must switch to an **ASGI** server and configure it to survive on Render's 512MB RAM limit.

---

## 📋 Table of Contents
1. [Update Dependencies](#1-update-dependencies)
2. [Configure `settings.py` for Production](#2-configure-settingspy-for-production)
3. [Create a Build Script](#3-create-a-build-script)
4. [Render Dashboard Configuration](#4-render-dashboard-configuration)
5. [Understanding Free Tier Limitations](#5-understanding-free-tier-limitations)

---

## 1. Update Dependencies

To run asynchronously and serve static files (like your Bootstrap CSS) on Render, you need a few new packages. 

Install these in your local environment:
```bash
pip install uvicorn whitenoise dj-database-url psycopg2-binary
```

Once installed, freeze your requirements so Render knows what to install:
```bash
pip freeze > requirements.txt
```
> **Note:** `uvicorn` is our ASGI server. `whitenoise` serves static files. `dj-database-url` and `psycopg2-binary` allow Django to connect to Render's PostgreSQL database.

---

## 2. Configure `settings.py` for Production

Open your `settings.py` and make the following critical adjustments for deployment.

### A. Allowed Hosts & Security
```python
import os

# DO NOT leave this as True in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Render's domain
ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', '127.0.0.1')]
```

### B. Add WhiteNoise for Static Files
Render does not have a built-in static file server, so Django must serve its own using WhiteNoise.

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add WhiteNoise right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middlewares
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable compression and caching support for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### C. Database Configuration
Update your database settings to use Render's database URL if it exists, otherwise fallback to SQLite (for local testing).

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}
```

---

## 3. Create a Build Script

Render needs to know how to build your app. Create a file named `build.sh` in the root of your project (next to `manage.py`):

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Make sure the script is executable. If you are on Mac/Linux, run this in your terminal:
```bash
chmod a+x build.sh
```

*(Commit and push all these changes to your GitHub/GitLab repository).*

---

## 4. Render Dashboard Configuration

Log into your Render dashboard and create a new **Web Service** linked to your repository. Use the following settings:

* **Name:** `my-django-inbox` (or whatever you prefer)
* **Environment:** `Python`
* **Region:** Choose the one closest to you.
* **Branch:** `main` (or `master`)
* **Build Command:** `./build.sh`
* **Start Command:** 
  ```bash
  uvicorn myproject.asgi:application --host 0.0.0.0 --port $PORT --workers 1
  ```
  *(⚠️ **CRITICAL:** Replace `myproject` with the actual name of your core Django folder where `asgi.py` lives. The `--workers 1` flag is mandatory to prevent your app from crashing due to the Free Tier's 512MB RAM limit).*
* **Plan:** Free

### Environment Variables
Under the **Environment** tab on Render, add the following variables:
1. `PYTHON_VERSION`: `3.10.0` (or whatever version you are using)
2. `DEBUG`: `False`
3. `SECRET_KEY`: *(Generate a random string of 50 characters and paste it here)*
4. `DATABASE_URL`: *(If you created a Render PostgreSQL database, paste its Internal Database URL here).*

Click **Create Web Service** and wait for the deployment to finish!

---

## 5. Understanding Free Tier Limitations

Once your app is live, keep these Render Free Tier quirks in mind when testing your real-time SSE inbox:

1. **The "Cold Start" Spin-Down:** If no one visits your site for 15 minutes, Render puts the server to sleep. The next time you open the app, it may take **50+ seconds** to load. During this wake-up time, your SSE connection will fail to connect, but will automatically retry and connect once the server is fully awake.
2. **The Connection Limit:** The free tier allows a maximum of **100 concurrent connections**. Since SSE keeps a connection permanently open, a maximum of 100 browser tabs can be listening to the inbox at the same time.
3. **Database Expiry:** Free Render PostgreSQL databases expire and are permanently deleted after **30 days**. This is great for class projects, but not for long-term production storage!
