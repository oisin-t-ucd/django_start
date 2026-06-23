# Django User Authentication: Practical Exercises


---

## Exercise 1: The Dynamic Dashboard (Template Logic)

Currently, our navigation bar changes based on whether a user is logged in or not. Now, let's apply that same logic to the main content of a page.

**Your Task:** Create a new "Dashboard" view and template that changes its content entirely based on the user's session state.

**Steps:**

1. Create a new view function called `dashboard` and map it to a `/dashboard/` URL route.
2. Create a template named `dashboard.html`.
3. Inside the template, use the `{% if user.is_authenticated %}` template tag.


4. **If the user is logged out:** Display a generic marketing message (e.g., "Welcome to our platform! Sign up today to access premium features.") and a link to the registration page.
5. **If the user is logged in:** The marketing message should disappear. Instead, display a personalized welcome message using `{{ user.username }}` and a mock table of data (e.g., "Recent Activity Logs" or "Your Account Statistics").



**Goal:** Understand that session state isn't just for blocking pages; it is a powerful tool for dynamically rendering HTML blocks within a single page.

---

## Exercise 2: The `?next=` Parameter Maze (Routing & Decorators)

Django's login view automatically keeps track of the page a user was attempting to access before being forced to log in. Let's test this functionality.

**Your Task:** Create a highly restricted view and test Django's automatic redirection system.

**Steps:**

1. Create a new view called `security_settings` and map it to a `/security/` URL route.
2. Protect this view by adding the `@login_required` decorator directly above the view function.


3. Ensure your `LOGIN_URL = 'login'` is properly set at the bottom of your `settings.py` file.


4. **The Test:** Log out of your application. Manually type `[http://127.0.0.1:8000/security/](http://127.0.0.1:8000/security/)` into your browser's address bar.
5. Verify that you are redirected to the login page and that the URL now contains `?next=/security/`.


6. Log in successfully and verify that you are taken directly to the security page instead of the default home page.



**Goal:** Prove that you understand how to restrict access to specific views and how Django handles the user experience of accessing protected routes.

---

## Exercise 3: User Feedback with Messages

In our class walkthrough, we added a success message that appears when a user successfully registers an account: `messages.success(request, f'Account created successfully, now you can login.')`.

**Your Task:** Expand the use of Django's messages framework to provide better user feedback across the entire authentication flow.

**Steps:**

1. Locate where your `LoginView` and `LogoutView` are defined in your `urls.py` file.


2. *Hint:* Because these are built-in class-based views, you cannot simply add `messages.success()` inside the view like we did for the custom `register` function. You will need to research how to add success messages to Django's `auth_views`.
3. Implement a feature where a message pops up (e.g., "Welcome back!") when a user successfully logs in.
4. Implement a feature where a message pops up (e.g., "You have been securely logged out.") when a user logs out.

**Goal:** Get comfortable interacting with Django's messaging middleware to improve the overall User Experience (UX).

---

## Exercise 4: Stretch Goal - Password Change View

We have successfully used `django.contrib.auth.views` to implement our `LoginView` and `LogoutView`. Django provides several other pre-built views for authentication.

**Your Task:** Implement the built-in Password Change functionality.

**Steps:**

1. Import and use `auth_views.PasswordChangeView` in your `urls.py` file, assigning it to a `/password-change/` route.
2. Pass a `template_name` argument to the view, pointing it to a new template (e.g., `users/password_change.html`), just like we did for the login and logout views.


3. Create the `password_change.html` template. Make sure to load the crispy forms tags `{% load crispy_forms_tags %}` and format your form using `{{ form|crispy }}`.


4. Add a link to the Password Change page in your navigation bar, ensuring it is only visible `{% if user.is_authenticated %}`.


5. *Note:* You will also need to configure where the user is redirected *after* a successful password change. Look into `PasswordChangeDoneView`.

**Goal:** Build confidence in using Django's official documentation and extending your app with built-in class-based views.