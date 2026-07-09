# Django Class-Based Views: Exercise Solutions

---

## Exercise 1: The Personal Dashboard (Overriding `get_queryset`)

To show only the posts belonging to the logged-in user, we need to intercept the database query before it is sent to the template.

### 1. The View (`views.py`)



```
python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class UserPostListView(LoginRequiredMixin, ListView):
model = Post
template_name = 'blog/user_posts.html'
context_object_name = 'posts'


    def get_queryset(self):
        # Instead of returning Post.objects.all(), we filter by the requested user
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')
```


### 2. The URL (`urls.py`)
```python
from django.urls import path
from .views import UserPostListView

urlpatterns = [
    # ... other paths
    path('my-posts/', UserPostListView.as_view(), name='user-posts'),
]

```

---

## Exercise 2: The Context Expansion (Overriding `get_context_data`)

To add extra data (like a post count) to a `DetailView`, we override `get_context_data`.

### 1. The View (`views.py`)

```python
from django.views.generic import DetailView
from .models import Post

class PostDetailView(DetailView):
    model = Post  
    
    def get_context_data(self, **kwargs):
        # 1. Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        
        # 2. Add our new data to the dictionary. 
        # self.object refers to the specific Post being viewed.
        author = self.object.author
        context['total_posts'] = Post.objects.filter(author=author).count()
        
        # 3. Return the updated context
        return context

```

### 2. The Template (`post_detail.html`)

You can now access `{{ total_posts }}` directly in your HTML.

```html
<div class="article-metadata">
    <a class="mr-2" href="#">{{ object.author }}</a>
    <span class="badge badge-info">This author has published {{ total_posts }} total posts.</span>
    <small class="text-muted">{{ object.date_posted|date:'dS, F, Y' }}</small>
</div>

```

---

## Exercise 3: The Search Feature (Handling GET parameters)

Here we extract the URL parameter (`?q=...`) and apply it to our ORM filters.

### 1. The Search Form (in your `base.html` or `home.html`)

```html
<form method="GET" action="{% url 'blog-home' %}">
    <input type="text" name="q" placeholder="Search posts...">
    <button type="submit">Search</button>
</form>

```

### 2. The View (`views.py`)

```python
from django.views.generic import ListView
from django.db.models import Q # Q objects allow for OR queries (Title OR Content)
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        # 1. Fetch the default queryset (which includes the ordering from above)
        qs = super().get_queryset()
        
        # 2. Check if there is a 'q' parameter in the URL (e.g., /?q=django)
        query = self.request.GET.get('q')
        
        # 3. If a query exists, filter the queryset
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            
        return qs

```

---

## Exercise 4: The Soft Delete (Overriding `delete`)

Soft deletes are a standard backend engineering practice to prevent accidental data loss while appearing deleted to the end user.

### 1. Update the Model (`models.py`)

```python
from django.db import models

class Post(models.Model):
    # ... existing fields
    is_deleted = models.BooleanField(default=False)

```

*(Don't forget to run `python manage.py makemigrations` and `python manage.py migrate`!)*

### 2. Update the DeleteView (`views.py`)

```python
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        # 1. Grab the specific post object
        self.object = self.get_object()
        
        # 2. Toggle the boolean flag instead of deleting from the database
        self.object.is_deleted = True
        self.object.save()
        
        # 3. Redirect the user to the success URL
        return HttpResponseRedirect(self.get_success_url())

```

### 3. Filter Out Deleted Posts (`views.py`)

Finally, update your `PostListView` so deleted posts no longer show up on the homepage.

```python
class PostListView(ListView):
    # ...
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Exclude softly deleted posts
        qs = qs.exclude(is_deleted=True)
        
        # ... your search logic from Exercise 3 can go here
        return qs

```

