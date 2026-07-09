# Django Profiles & Architecture: Practical Exercises

Welcome to your practical exercises for User Profiles and Media Handling! Having completed the walkthrough and read through the Advanced Architecture guide, it is time to put those concepts into practice.

These tasks will challenge you to write efficient database queries, manage file storage intelligently, and make deliberate architectural choices.

---

## Exercise 1: Taming the Uploads (Image Optimization)

In the advanced guide, we discussed how unoptimized image uploads can destroy a server's storage and bandwidth. Let's fix that by utilizing the `Pillow` library we installed.

**Your Task:** Override the `save()` method on your `Profile` model to automatically resize any uploaded image to a maximum of 150x150 pixels.

**Steps:**

1. Open `users/models.py` and import `Image` from the `PIL` library.
2. Define the `save(self, *args, kwargs)` method inside your `Profile` class.
3. Ensure you call `super().save(*args, kwargs)` first so the image is temporarily saved to the file system.
4. Use `Image.open()` to open the file, check its dimensions, and use the `.thumbnail()` method to resize it if it exceeds 150px in height or width.
5. Save the resized image back to the original file path.
6. **The Test:** Find a large, high-resolution image (e.g., 2MB or larger). Log in to the admin panel and upload it as a user's profile picture. Check your `media/profile_pics` directory on your computer to verify that the file size has been drastically reduced and the dimensions are capped at 150x150.

**Goal:** Understand how to intercept and modify model data right before (or immediately after) it hits the database or file system.

---

## Exercise 2: The N+1 Hunt (Database Efficiency)

It is time to prove that the N+1 database query problem is real and solve it using Django's ORM.

**Your Task:** Create a "Community Directory" page that lists all registered users and their profile pictures, ensuring you fetch the data in a single, efficient query.

**Steps:**

1. Create a new view function called `user_directory` in `users/views.py`.
2. Map this view to a `/community/` URL route in your `urls.py`.
3. Create a template (`users/user_directory.html`) that loops through the users and displays their username, email, and profile picture.
4. **The Trap:** First, write the view using `User.objects.all()`.
5. **The Fix:** Now, refactor your view query to use `User.objects.select_related('profile').all()`.
6. **The Test (Optional but Recommended):** If you want to see the difference with your own eyes, temporarily print the connection queries in your view to see the database hits drop from dozens down to just one:
```python
from django.db import connection
# Run your query...
# print(len(connection.queries))

```



**Goal:** Learn how to use `select_related()` to perform SQL JOINs and write performant, production-grade database queries.

---

## Exercise 3: The Explicit Refactor (Architectural Trade-offs)

We used Django Signals (`post_save`) to automatically create a Profile when a User is created. While elegant, signals can make debugging difficult because they hide the execution flow. Let's try the alternative approach.

**Your Task:** Disable the signal and refactor your registration view to explicitly handle profile creation.

**Steps:**

1. Open `users/apps.py` and comment out the `def ready(self):` block so your signals no longer fire.
2. **The Test:** Register a new user on your site. Go to the admin panel. You should notice that the new user exists, but they do *not* have an associated profile.
3. Open `users/views.py` and import the `Profile` model.
4. Locate your `register` view. Right after `form.save()` successfully creates a new user object, explicitly create a new Profile object for that user right there in the view.
5. **The Re-Test:** Register another new user. Verify in the admin panel that their profile was successfully generated via the view logic.

**Goal:** Understand that there are multiple ways to solve a problem in Django, and writing explicit, readable logic in your views is often preferable to relying on "invisible" signals.

---

## Exercise 4: Graceful Fallbacks (Template Logic)

Currently, our system relies on the `default.jpg` fallback being set in the model (`default='default.jpg'`). But what if a user manages to delete their profile entirely, or an image file goes missing from the server? A broken image icon creates a terrible user experience.

**Your Task:** Update your profile template to use a fallback default image if `user.profile.image` returns an error or is empty.

**Steps:**

1. Locate the `users/profile.html` template.
2. Find the `<img>` tag where the profile picture is rendered.
3. Wrap the image rendering in an `{% if %} / {% else %}` block.
4. Check if the user has a profile and an associated image URL. If they do, render it.
5. If they do not, hardcode the `src` attribute to point directly to `/media/default.jpg`.

**Goal:** Build resilient front-end templates that account for missing database relations or file system errors without breaking the user interface.