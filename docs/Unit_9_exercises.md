# Django Profile Update & CRUD: Practice Exercises

---

## Exercise 1: The "Bio" Expansion (Custom Validation)
**Goal:** Practice modifying models, updating ModelForms, and writing custom validation logic.

* **The Task:** Add a new `bio` text field to your `Profile` model. After updating the model, run your migrations (`makemigrations` and `migrate`). Then, update the `ProfileUpdateForm` to include this new field so users can fill it out on the frontend.
* **The Challenge:** We want to keep bios professional. Add a custom validation method to the form (e.g., `clean_bio(self)`) that checks the text. If the bio contains a specific forbidden word (you pick the word!), or if it exceeds 50 words, raise a `ValidationError` to prevent the form from saving and display a helpful error message to the user.

[clean method docs](https://docs.djangoproject.com/en/5.2/ref/forms/validation/)

---

## Exercise 2: The Standalone Contact Form (Standard Forms)
**Goal:** Contrast `ModelForm` with `forms.Form` to appreciate the heavy lifting the ORM does for you.

* **The Task:** Create a new "Contact Us" page. Instead of saving a message to the database, this form should use a standard `forms.Form` (not a ModelForm) with fields for a `name`, `email`, and a `message` body.
* **The Challenge:** In your view, handle the POST request. If the form `is_valid()`, do not save anything to the database. Instead, simply `print()` the `cleaned_data` dictionary to your terminal console so you can see the parsed data. Finally, use the Django `messages` framework to flash a success alert to the user and redirect them back to the contact page (using the Post/Get/Redirect pattern).

---

## Exercise 3: The Public Profile (CRUD - Read Operation)
**Goal:** Practice dynamic URL routing and the "Read" operation without the complexity of forms.

* **The Task:** Currently, the `/profile/` route is strictly for the logged-in user to edit their own data. Create a new, public-facing route like `/user/<str:username>/`. This page should display that specific user's profile picture, username, and email.
* **The Challenge:** Use Django's `get_object_or_404` shortcut in your view. If someone types in `/user/batman/` and Batman does not exist in your database, the app should throw a proper 404 "Page Not Found" error rather than crashing the server with a `DoesNotExist` exception.

---

## Exercise 4: The "Danger Zone" (CRUD - Delete Operation)
**Goal:** Safely implement the final piece of the CRUD puzzle.

* **The Task:** Add a red "Delete Account" button to the bottom of the profile update page. Clicking it should *not* delete the account immediately. Instead, it should take the user to a dedicated confirmation template (e.g., "Are you sure you want to delete your account? Yes/No").
* **The Challenge:** If the user confirms by submitting a POST request on the confirmation page, delete the `request.user` object (which will automatically delete the associated Profile). However, you must explicitly call Django's `logout(request)` function before redirecting them to the home page. If you don't log them out, the browser will hold onto a dead session cookie and cause errors!

[logout function docs](https://docs.djangoproject.com/en/5.2/topics/auth/default/)

---

## Exercise 5: The Bouncer: File Size Validation
**Goal:** Deepen your form validation logic and practice defensive programming.

* **The Task:** In the previous walkthrough, we used the Pillow library to resize images *after* they were saved to the file system. Now, let's stop massive files at the door before they even get saved.
* **The Challenge:** Write a `clean_image` method inside your `ProfileUpdateForm`. This method should check the incoming file size (`self.cleaned_data.get('image').size`). Note that the size is in bytes. If the file is larger than 2MB, raise a `ValidationError` (e.g., "File too large. Size should not exceed 2MB.") preventing the form from saving entirely.

---

