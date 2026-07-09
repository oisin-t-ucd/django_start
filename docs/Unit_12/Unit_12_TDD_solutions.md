# Unit 12 Lab: TDD Exercises (Solutions Guide)

This document contains the solutions for the Test-Driven Development lab. Remember, there are many ways to solve a problem in programming. If your code looks slightly different but your tests pass and cover the requirements, you have successfully completed the TDD loop!

---

## Exercise 1: The Reading Time Estimator (Model TDD)

### Phase 1: Red (The Test)

First, we write the test in `blog/tests.py` to assert what we expect the `get_read_time` method to return.

```python
# blog/tests.py

def test_get_read_time(self):
    # Create a post with exactly 400 words
    long_post = Post.objects.create(
        author=self.user,
        title='A Long Read',
        content='word ' * 400 
    )
    
    # We expect 400 words / 200 words-per-minute = 2 minutes
    self.assertEqual(long_post.get_read_time(), 2)
    
    # Edge case: Test an empty post to ensure it doesn't crash
    empty_post = Post.objects.create(
        author=self.user,
        title='Empty',
        content=''
    )
    self.assertEqual(empty_post.get_read_time(), 0)

```

*Run the test. It will fail with an `AttributeError`.*

### Phase 2 & 3: Green & Refactor (The Implementation)

Next, we implement the method in `blog/models.py`.

```python
# blog/models.py
import math

class Post(models.Model):
    # ... existing fields ...

    def get_read_time(self):
        if not self.content:
            return 0
        
        # Split the string by spaces to get a list of words, then count them
        word_count = len(self.content.split())
        
        # Divide by 200 and round up to the nearest whole minute
        minutes = math.ceil(word_count / 200)
        
        return minutes

```

> **Note:** Why use `math.ceil` instead of `round()`? If a post has 201 words, it technically takes 1.005 minutes to read. `round()` would round it down to 1, but `math.ceil` ensures that even slightly over a minute gets bumped to a "2 min read", which is standard UX practice for blogs.

---

## Exercise 2: The Drafts Filter (View TDD)

### Phase 1: Red (The Test)

We write a test in `blog/tests.py` to ensure unpublished posts do not appear on the home page.

```python
# blog/tests.py

def test_home_view_hides_drafts(self):
    # Create one published post and one draft
    Post.objects.create(
        author=self.user,
        title='Published Post',
        content='This should be visible.',
        is_published=True
    )
    Post.objects.create(
        author=self.user,
        title='Hidden Draft',
        content='This should NOT be visible.',
        is_published=False
    )
    
    response = self.client.get(reverse('blog-home'))
    
    # Assertions
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Published Post')
    self.assertNotContains(response, 'Hidden Draft')

```

*Run the test. It will fail because `is_published` does not exist yet.*

### Phase 2: Green (The Implementation)

First, update the model and migrate the database.

```python
# blog/models.py

class Post(models.Model):
    # ... existing fields ...
    is_published = models.BooleanField(default=True)

```

Then, update the query in `blog/views.py`. If you are using a generic `ListView`, it looks like this:

```python
# blog/views.py

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    
    # Override the default queryset to only show published posts
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-date_posted')

```

---

## Exercise 3: The "No Duplicates" Validator (Form TDD)

### Phase 1: Red (The Test)

We test the `post-create` view in `blog/tests.py` to ensure it rejects a duplicate title.

```python
# blog/tests.py

def test_prevent_duplicate_post_titles(self):
    self.client.login(username='testuser', password='12345')
    
    # Create the first post
    Post.objects.create(
        author=self.user,
        title='My Awesome Journey',
        content='Original text.'
    )
    
    # Attempt to POST a second post with the exact same title
    response = self.client.post(reverse('post-create'), {
        'title': 'My Awesome Journey',
        'content': 'Some new text.'
    })
    
    # If the form is invalid, it re-renders the page (200 OK). 
    # If it bypasses validation and saves, it redirects (302 Found).
    self.assertEqual(response.status_code, 200)
    
    # Verify the error message is present
    self.assertFormError(response, 'form', 'title', 'You already have a post with this title.')

```

*Run the test. It will fail with a `302 != 200` error.*

### Phase 2 & 3: Green & Refactor (The Implementation)

To validate this, we need a custom form in `blog/forms.py` that checks the database.

```python
# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        # Check if any post with this title already exists in the database
        # (For simplicity in this exercise, we check globally. In a real app, 
        # you would filter by the specific author).
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError('You already have a post with this title.')
            
        return title

```

Next, ensure your view is actually using this form. In `blog/views.py`:

```python
# blog/views.py
from .forms import PostForm

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm # Tell the view to use our custom form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

```

> **Note:** The `clean_title` method above checks if *anyone* has used the title. To strictly check if the *current user* has used it, you would need to pass the `request.user` into the form via the view's `get_form_kwargs` method. If you solved it the simple way above, you met the core requirement of the exercise!

