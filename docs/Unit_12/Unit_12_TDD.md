# Unit 12 Lab: Test-Driven Development (TDD) Walkthrough

Usually, when we build an application, we write the code first and then test it to see if it works. Test-Driven Development (TDD) flips this entire process upside down. In TDD, you write the test *before* you write the feature.

At first, this will feel completely backward. It is like grading an exam before the student has even taken it. However, adopting this mindset will force you to clearly define what your code needs to do before you get lost in the weeds of writing it.

---

## 1. The Core Loop: Red, Green, Refactor

TDD is built on a continuous, three-step cycle. Professional engineering teams use this exact rhythm every day.

| Phase | Action | Goal |
| --- | --- | --- |
| **1. Red** | Write a test for a feature that does not exist yet, then run the test suite. | To see the test fail. This proves your test is actually checking for something missing. |
| **2. Green** | Write the absolute minimum amount of application code required to make the test pass. | To get a passing test suite. Do not worry about writing perfect code yet. |
| **3. Refactor** | Clean up your code, improve variable names, and optimize performance. | To improve code quality while relying on the passing test as your safety net. |

---

## 2. Walkthrough: Building an "About" Page with TDD

Let's put this into practice. Our goal is to add a simple "About" page to our Blog application. Instead of going straight to `views.py`, we are starting in `tests.py`.

### Step 1: The Red Phase

Open your `blog/tests.py` file and add a new test to the `PostViewsTests` class. We are going to assert that if a user visits `/about/`, they get a `200 OK` status and see the `blog/about.html` template.

```python
# blog/tests.py

def test_about_page_view(self):
    url = reverse('blog-about')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/about.html')

```

Now, run your tests in the terminal:

```bash
python manage.py test blog

```

**The Result:** You will get a giant error ending with `django.urls.exceptions.NoReverseMatch: Reverse for 'blog-about' not found`. This is a successful "Red" phase! The test failed exactly as expected because the URL does not exist yet.

### Step 2: The Green Phase

Now, we write the minimum code necessary to make that error go away. We need a URL, a View, and a Template.

First, create the view in `blog/views.py`:

```python
# blog/views.py

def about(request):
    return render(request, 'blog/about.html')

```

Next, wire up the URL in `blog/urls.py`:

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... your other urls
    path('about/', views.about, name='blog-about'),
]

```

Finally, create a basic template file at `blog/templates/blog/about.html`:

```html
<h1>About Our Blog</h1>
<p>We write about web development.</p>

```

Run your tests again:

```bash
python manage.py test blog

```

**The Result:** `OK`. You have successfully reached the "Green" phase.

### Step 3: The Refactor Phase

Now we look at our code and ask: *Can this be cleaner?* In Django, rendering a static HTML template doesn't actually require a custom function view. We can use Django's built-in `TemplateView` directly in the URLs file to save space.

Let's refactor `blog/urls.py`:

```python
# blog/urls.py
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # ... your other urls
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='blog-about'),
]

```

Since we moved the logic to the URL, we can now delete the `about` function we just wrote in `blog/views.py`.

Run the tests one more time:

```bash
python manage.py test blog

```

**The Result:** Still `OK`! You just deleted code and completely changed the routing architecture, but because you had a test protecting you, you can be 100% confident that the page still works exactly as requested.

---

## 3. Walkthrough: Adding Business Logic to a Model

TDD shines brightest when calculating logic. Let's add a feature to our `Post` model that checks if a post is considered "new" (published within the last 24 hours).

### Step 1: The Red Phase

We expect our `Post` instances to have a method called `is_new()`. Let's test it in `blog/tests.py`.

```python
# blog/tests.py
from django.utils import timezone
import datetime

class PostModelTests(TestCase):
    # ... your existing setup ...

    def test_is_new_post(self):
        # Create a post dated right now
        recent_post = Post.objects.create(
            author=self.user, 
            title='Recent Post', 
            content='Posted just now.'
        )
        self.assertTrue(recent_post.is_new())

        # Create a post dated 3 days ago
        old_time = timezone.now() - datetime.timedelta(days=3)
        old_post = Post.objects.create(
            author=self.user, 
            title='Old Post', 
            content='Posted ages ago.'
        )
        # We manually override the auto_now_add date for testing
        old_post.date_posted = old_time 
        old_post.save()

        self.assertFalse(old_post.is_new())

```

Run the tests. **Result:** `AttributeError: 'Post' object has no attribute 'is_new'`. Perfect. We are in the Red.

### Step 2: The Green Phase

Let's add the logic to our `Post` model in `blog/models.py`.

```python
# blog/models.py
from django.utils import timezone
import datetime

class Post(models.Model):
    # ... your existing fields ...

    def is_new(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        return self.date_posted >= yesterday

```

Run the tests again. **Result:** `OK`. We are in the Green.

### Step 3: The Refactor Phase

The code in `models.py` is clean, readable, and doing exactly what it should. No major refactoring is needed here, which often happens when you write small, targeted functions.

> **Why did we do it this way?**
> If we had written the model method first, we might have forgotten to test the edge case of an older post returning `False`. By writing the test first, we defined the exact boundaries of how the feature should behave before writing a single line of application logic.