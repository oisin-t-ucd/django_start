import os

import django

# 1. Setup the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_start.settings")
django.setup()

from django.contrib.auth.models import User

from users.models import Profile

users = User.objects.all()
count = 0
for user in users:

    try:
        Profile.objects.create(user=user)
        print(f"created user for {user.username}")
        count += 1
    except Exception as exc:
        print(f"issue creating profile for {user.username} - {exc}")

print(f"successfully created {count} profiles")
