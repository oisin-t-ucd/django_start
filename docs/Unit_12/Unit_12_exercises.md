# Unit 12 Lab: Django Testing in Practice

Now that we have walked through the core concepts of automated testing in Django, it is time to put these principles into practice. These exercises are designed to scale in difficulty—starting with straightforward form validation and ending with a real-world debugging scenario.

Work through these in order within your project environment.

---

## Exercise 1: Testing the "Sad Path" (Form Validation)

In the walkthrough, we tested what happens when a user submits perfectly valid data (`test_user_register_form`). However, a robust test suite must also verify that the application correctly rejects invalid data—often called "sad path" testing.

**The Task:** Write a new test method inside your `UserFormsTests` class that verifies the registration form fails when the passwords do not match.

**Instructions:**

1. Create a new method named `test_user_register_form_mismatched_passwords`.
2. Create a `form_data` dictionary where `password1` and `password2` are different.
3. Instantiate the `UserRegisterForm` with this data.
4. Assert that the form is *invalid*.

**Starter Code:**

```python
def test_user_register_form_mismatched_passwords(self):
    # 1. Set up your invalid form_data dictionary here
    
    # 2. Pass the data to UserRegisterForm
    
    # 3. Write your assertion here (Hint: You want to assert False)
    pass

```

---

## Exercise 2: The 404 Edge Case (View Testing)

Our current test suite verifies that `test_post_detail_view` returns a `200 OK` status when requesting a post that exists in the database. But what happens if a user navigates to a broken link or requests a post ID that doesn't exist?

**The Task:**
Write a test to ensure your application gracefully handles a request for a non-existent post by returning a `404 Not Found` status.

**Instructions:**

1. Create a new method named `test_post_detail_view_not_found` inside your `PostViewsTests` class.
2. Use the `reverse()` function to target the `post-detail` URL, but pass it an ID that is guaranteed *not* to be in your test database (e.g., `id=999`).
3. Simulate a GET request using the test client.
4. Assert that the response `status_code` equals `404`.

---

## Exercise 3: The Authentication Debugging Challenge

It is incredibly common in the industry to inherit a failing test written by someone else. The following test was written to check the post creation view, but it is currently failing and returning a `302 Found` (redirect) status code instead of the expected `200 OK`.

**The Task:**
Diagnose and fix the broken test.

**Instructions:**

1. Copy the code block below into your `PostViewsTests` class.
2. Run your test suite. Read the traceback carefully.
3. *Hint:* Why would a view responsible for creating a new post immediately redirect a user before they even see the form? Think about what state the test `client` is in by default.
4. Add the missing line of code to make the test pass.

**The Broken Code:**

```python
def test_create_post_view_unauthorized(self):
    # A previous developer wrote this test, but it is failing!
    # Fix the code below so that the test client successfully reaches the post creation form.
    
    response = self.client.get(reverse('post-create'))
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

```

---

## Exercise 4: The Coverage Scavenger Hunt

Automated tests are only useful if they actually cover the code you have written. In this final exercise, you will use `coverage.py` to identify untested logic and write a test to cover it.

**The Task:**
Generate an HTML coverage report, find a gap in your testing, and write a targeted test to close it.

**Instructions:**

1. Open your integrated terminal (e.g., in VS Code) and run your tests using the coverage tool:
```bash
coverage run manage.py test

```


2. Generate the interactive HTML report:
```bash
coverage html

```


3. Open the newly created `htmlcov/index.html` file in your web browser.
4. Click through your `models.py` and `views.py` files. Find **one specific line or block of code** that is highlighted in red (indicating it was never executed during your tests).
5. Write a single test function in the appropriate `tests.py` file specifically designed to turn that red line green.
6. Re-run steps 1 and 2 to verify your coverage percentage has increased.