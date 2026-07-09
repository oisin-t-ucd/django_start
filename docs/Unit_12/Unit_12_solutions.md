# Unit 12 Solutions: Django Testing in Practice

This document contains the solutions and explanations for the Django testing exercises.

## Exercise 1: Testing the "Sad Path" (Form Validation)

**Objective:** Verify that `UserRegisterForm` correctly invalidates a submission when the passwords do not match.

**Solution:**

```python
def test_user_register_form_mismatched_passwords(self):
    # 1. Set up your invalid form_data dictionary here
    form_data = {
        'username': 'newuser', 
        'email': 'newuser@example.com', 
        'password1': 'django1234', 
        'password2': 'wrongpassword123' # Passwords do not match
    }
    
    # 2. Pass the data to UserRegisterForm
    form = UserRegisterForm(data=form_data)
    
    # 3. Write your assertion here (Hint: You want to assert False)
    self.assertFalse(form.is_valid())

```

**Why it works:** `form.is_valid()` runs Django's built-in validation checks, including the `clean()` methods defined on the form. Since `password1` and `password2` do not match, the form gathers errors and `is_valid()` evaluates to `False`. Using `self.assertFalse()` ensures the test passes *because* the validation failed.

---

## Exercise 2: The 404 Edge Case (View Testing)

**Objective:** Ensure the application returns a `404 Not Found` status when a user requests a post ID that does not exist.

**Solution:**

```python
def test_post_detail_view_not_found(self):
    # We use an ID like 999 to guarantee it does not exist in the test DB
    url = reverse('post-detail', args=[999])
    
    # Simulate a GET request
    response = self.client.get(url)
    
    # Assert that the view responds with a 404 Not Found status
    self.assertEqual(response.status_code, 404)

```

**Why it works:** If your Django view uses `get_object_or_404(Post, pk=id)` or a class-based `DetailView`, the framework automatically raises an `Http404` exception when a database record isn't found. The test client captures this and correctly assigns the `404` status code to the response.

---

## Exercise 3: The Authentication Debugging Challenge

**Objective:** Fix a broken test that receives a `302 Found` (redirect) instead of a `200 OK` when accessing a protected view.

**Solution:**

```python
def test_create_post_view_unauthorized(self):
    # Fix: The test client must simulate a logged-in user to access protected routes.
    self.client.login(username='testuser', password='12345')
    
    response = self.client.get(reverse('post-create'))
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

```

**Why it works:** Views that create, update, or delete data usually require a user to be logged in (often enforced via the `@login_required` decorator or `LoginRequiredMixin`). If an unauthenticated user tries to access these routes, Django automatically redirects them to the login page (yielding a `302` status code). Adding `self.client.login(...)` before the request fixes the issue.

---

## Exercise 4: The Coverage Scavenger Hunt

**Objective:** Identify untested lines of code using `coverage.py` and write tests to cover them.

*Note: The exact solution will vary based on the specific gaps in your codebase, but here is a representative example of how to solve a common coverage gap.*

**Example Scenario:** Upon viewing the `htmlcov/index.html` report, you notice that the `__str__` method for the `Profile` model in `users/models.py` is highlighted in red.

**Example Code Gap (`users/models.py`):**

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' # <-- highlighted in red

```

**Example Solution (`users/tests.py`):**
To turn that line green, write a test that explicitly calls the string representation of the model:

```python
def test_profile_str_method(self):
    # Assuming setUp() already created self.user and self.user.profile
    profile = self.user.profile
    
    # Assert that str(profile) matches the expected output
    expected_string = f'{self.user.username} Profile'
    self.assertEqual(str(profile), expected_string)

```

**Why it works:** Test coverage tools track which lines of code are executed during the test suite run. Simply instantiating the model isn't enough; to test the `__str__` method, it must be explicitly invoked (using `str()`), which fulfills the execution requirement and increases the coverage percentage.