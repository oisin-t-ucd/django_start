# Unit 12 Lab: Test-Driven Development (TDD) Exercises

Now that you have walked through the mechanics of Test-Driven Development, it is time to build muscle memory. Remember, the goal of TDD is not just to write tests, but to let the tests design your code.

For each of the exercises below, you must strictly follow the **Red, Green, Refactor** cycle. Do not touch your `models.py`, `views.py`, or `forms.py` files until you have a failing test in your terminal!

These exercises feature a "low-floor, high-ceiling" progression. They start with a simple calculation and scale up to complex database queries and form validations.

---

## Exercise 1: The Reading Time Estimator (Model TDD)

Many modern blogs tell the user how long an article will take to read (e.g., "5 min read"). Let's build this feature for our `Post` model. The average reading speed is roughly 200 words per minute.

**The Task:** Drive the creation of a `get_read_time()` method on the `Post` model using TDD.

**Phase 1: Red (The Test)**

1. Open `blog/tests.py` and find your `PostModelTests` class.
2. Write a new method called `test_get_read_time`.
3. Create a test `Post` instance with a `content` string that is exactly 400 words long.
*(Pro Tip: You don't need to type 400 words. You can use Python string multiplication: `'word ' * 400`)*.
4. Assert that `post.get_read_time()` equals `2`.
5. Run your test suite. You should get an `AttributeError` because the method doesn't exist.

**Phase 2: Green (The Implementation)**

1. Open `blog/models.py`.
2. Add the `get_read_time(self)` method to the `Post` class.
3. Write the minimum logic to calculate the word count of `self.content`, divide by 200, and return the rounded integer.
4. Run your tests. They should pass!

**Phase 3: Refactor**
Look at your method. Can the math be cleaner? Does it handle empty strings properly without crashing? Make any adjustments while relying on your passing test as a safety net.

---

## Exercise 2: The Drafts Filter (View TDD)

Right now, every time a user creates a post, it goes live immediately. We want to add a "Draft" feature so writers can save work without publishing it to the homepage.

**The Task:** Ensure that the homepage view (`blog-home`) only displays published posts, completely ignoring drafts.

**Phase 1: Red (The Test)**

1. Open `blog/tests.py` and navigate to `PostViewsTests`.
2. Write a new method called `test_home_view_hides_drafts`.
3. Create *two* posts in this test:
* Post A: `title='Published Post'`, `is_published=True`
* Post B: `title='Hidden Draft'`, `is_published=False`


4. Simulate a GET request to the `blog-home` URL.
5. Assert that the response contains "Published Post".
6. Assert that the response does *not* contain "Hidden Draft" (`self.assertNotContains(response, 'Hidden Draft')`).
7. Run the test. It will fail, likely because `is_published` isn't a valid field yet, or because the draft leaks onto the page.

**Phase 2: Green (The Implementation)**

1. Open `blog/models.py` and add `is_published = models.BooleanField(default=True)` to the `Post` model.
2. Run `python manage.py makemigrations` and `python manage.py migrate` to update your database.
3. Open `blog/views.py`. Update your home view's query so it fetches `Post.objects.filter(is_published=True)`.
4. Run your tests. You should see a beautiful line of passing dots.

---

## Exercise 3: The "No Duplicates" Validator (Form TDD)

We want to prevent users from accidentally submitting the exact same post twice. If a user tries to submit a post with a title they have already used, the form should throw a validation error.

**The Task:** Use TDD to build a custom validator in the `PostForm` that blocks duplicate titles by the same author.

**Phase 1: Red (The Test)**

1. Open `blog/tests.py`.
2. Create a test user and immediately give them a post with the title `'My Awesome Journey'`.
3. Simulate an authenticated POST request to the `post-create` view, submitting a new post with the exact same title: `'My Awesome Journey'`.
4. Assert that the response status code is `200` (meaning the form failed validation and re-rendered the page, rather than returning a `302` redirect).
5. (Optional stretch goal): Assert that the form's error dictionary contains a message about duplicate titles.
6. Run the test. It will fail because the view currently accepts the duplicate post and redirects (`302`).

**Phase 2: Green (The Implementation)**

1. Open `blog/forms.py` (you may need to create this and link it to your view if you were relying purely on generic views).
2. Write a `clean_title` method inside the form.
3. Add a query inside `clean_title` that checks if a post with that title already exists for the currently logged-in user. If it does, raise a `forms.ValidationError`.
4. Run the tests until the form correctly rejects the duplicate data.

---

> **💻 Developer Environment Quick Tip:** > Running tests continuously can feel tedious if you have to keep reaching for your mouse. If you are using a Mac and VS Code, use the keyboard shortcut **`Cmd + \``** (Command + backtick) to instantly toggle your integrated terminal open and closed. Press the **Up Arrow** in the terminal to retrieve your last command (`python manage.py test`), and hit **Enter**. This keeps your hands on the keyboard and speeds up the Red-Green-Refactor loop tremendously!