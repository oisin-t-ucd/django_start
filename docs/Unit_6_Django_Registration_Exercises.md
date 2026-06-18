# Django Authentication: In-Class Exercises

These exercises are designed to help you practice what we just covered regarding user registration, form customization, and database management. Do not move on to the next exercise until you have completed the current one and understand why it works.

---

## Exercise 1: The "Broken Code" Challenge

**Scenario:** You have joined a team, and the previous developer left the registration page in a broken state. Users are complaining that they cannot sign up.

**Your Task:**
Below is the code for the `register` view. It contains **three specific errors**. Identify and fix them so the registration process works correctly.

```python
# users/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm() # ERROR 1 is here
        if form.is_valid():
            # ERROR 2 is missing here
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html') # ERROR 3 is here
```

**Hints:**
1. How does the form know what the user typed in?
2. What actually commits the new user to the database?
3. How does the template get access to the `form` variable so it can render it with `{{ form|crispy }}`?

---

## Exercise 2: Database Inspection & Manipulation

**Scenario:** As a backend developer, you cannot just trust that the web interface is working; you need to verify how the data is actually structured and stored in the database. 

**Your Task:**
Use the **SQLite VS Code extension** to inspect the users you have created and modify their permissions directly in the database.

1.  **Open the Database:** Press `Ctrl+Shift+P` (or `Cmd+Shift+P`), type `SQLite: Open Database`, and select your `db.sqlite3` file.
2.  **Inspect the Table:** In the VS Code Explorer panel, expand the SQLITE EXPLORER section and open the `auth_user` table. 
3.  **Analyze the Fields:** Locate the user you just registered. 
    * Look at the `password` column. Notice how Django automatically applied a hashing algorithm (PBKDF2 by default) so the plain text is never stored.
    * Look at the boolean columns: `is_superuser`, `is_staff`, and `is_active`. They should currently be set to `0` (False).
4.  **The Hacker Challenge:** Directly in the SQLite explorer, change the `is_staff` value for your new user from `0` to `1`. Save the database changes. 
5.  **Verify the Hack:** Run your Django server, navigate to `http://127.0.0.1:8000/admin`, and try to log in with that user. Because you manually flipped the `is_staff` bit in the database, they should now have access to the admin dashboard!

---

## Exercise 3: Form Customization (Adding First & Last Name)

**Scenario:** We need to collect the user's actual name during registration, not just their email and username.

**Your Task:**
Modify the `UserRegisterForm` we created in `users/forms.py` to include the `first_name` and `last_name` fields.

**Requirements:**
1.  Both fields should be mandatory (required).
2.  Update the `Meta` class so these fields appear on the form *between* the username and the email.

**Hints:**
* You will need to add new variables to the class using `forms.CharField()`. Look at how the `email` field was added.
* The order of the strings in the `fields` list inside the `Meta` class dictates the order they render on the page.

---

## Exercise 4: Defensive Redirection

**Scenario:** Currently, if a logged-in user navigates to `/register`, they are presented with the registration form again. This is poor UX and can lead to session confusion.

**Your Task:**
Update the `register` view in `users/views.py` so that if a user is *already authenticated*, they are immediately redirected back to the `blog-home` page with a warning message.

**Requirements:**
1.  Use `request.user.is_authenticated` at the very beginning of your view to check their status.
2.  If true, use `messages.warning()` to display: "You already have an account!"
3.  Redirect them to `'blog-home'`.

**Test it:** Create an account (which logs you in or sets up your session), then manually type `/register` into your URL bar. You should bounce back to the home page and see the warning alert.
