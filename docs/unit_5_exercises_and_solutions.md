# Django Database Lab: Exercises & Solutions

Work through the following exercises to solidify your understanding of Django Models, Migrations, and the ORM. You will need your terminal and the Django shell (`python manage.py shell`).

---

## Exercise 1: The "Non-Nullable" Migration Challenge

**Objective:** Handle adding a required field to a table that already contains data.

**Instructions:**

1. Open `blog/models.py`.
2. Add a new field to your `Post` model called `status`. It should be a `CharField` with a `max_length` of 20. Do **not** provide a `default` argument.
```python
status = models.CharField(max_length=20)

```


3. Run `python manage.py makemigrations`.
4. You will be faced with a prompt warning you that you are trying to add a non-nullable field without a default to a model that already exists.
5. Choose the option to provide a one-off default value directly in the terminal, and type `'Draft'` (include the quotes!).
6. Apply the migration.

**What Happened:**
When you ran `makemigrations`, Django saw that older `Post` rows in the database wouldn't have a value for this new required `status` column. Since databases hate empty required columns, Django paused and asked:

```text
It is impossible to add a non-nullable field 'status' to post without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.

```

**The Fix:**
You selected `1`. The terminal then opened a Python prompt:

```text
Please enter the default value as valid Python.
The datetime and django.utils.timezone modules are available, so it is possible to provide e.g. timezone.now as a value.
Type 'exit' to exit this prompt
>>> 'Draft'

```

You entered `'Draft'`, which told Django to populate all existing database rows with the word "Draft". Finally, running `python manage.py migrate` successfully updated the database schema.

---

## Exercise 2: QuerySet Chaining & Exclusion

**Objective:** Practice chaining ORM methods to perform complex queries.

**Instructions:**

1. Ensure you have at least two Users in your database.
2. Create 5-6 different `Post` objects across these two users. Make sure at least one post has the word "Test" in the title.
3. Open the Django shell.
4. Write a single chained QuerySet that does the following:
* Finds all posts by your first User.
* **Excludes** any posts where the title contains the word "Test".
* Orders the remaining results by `date_posted` in **descending** order (newest first).



```python
from blog.models import Post
from django.contrib.auth.models import User

# 1. Grab the user
user_a = User.objects.first()

# 2. Write the chained QuerySet
# Use __icontains for case-insensitive matching
# Use a negative sign '-' in order_by for descending order
results = Post.objects.filter(author=user_a).exclude(title__icontains='Test').order_by('-created_on')

print(results)

```

---

## Exercise 3: Many-to-Many Relationships

**Objective:** Implement and interact with a Many-to-Many relationship.

**Instructions:**

1. In `blog/models.py`, create a new model named `Tag` that has a single field: `name` (a `CharField` with `max_length=50`). Don't forget the `__str__` method.
2. Update the `Post` model to include a `ManyToManyField` linking to `Tag`.
3. Make and apply your migrations.
4. Open the Django shell. Create two new `Tag` objects (e.g., "Python", "Django").
5. Fetch the first `Post` in your database and attach both tags to it.

**1. Update `models.py`:**

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    # ... previous fields ...
    # Tag is passed as a string because it's defined above, 
    # but could be passed directly if Tag is defined before Post.
    tags = models.ManyToManyField(Tag) 

```

**2. Terminal Commands:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py shell

```

**3. Shell Interactions:**

```python
from blog.models import Post, Tag

# Create tags
tag1 = Tag.objects.create(name='Python')
tag2 = Tag.objects.create(name='Django')

# Fetch a post
post = Post.objects.first()

# Add tags to the post
# Note: With ManyToMany, you use .add(), not standard assignment (=)
post.tags.add(tag1, tag2)

# Verify they were added
print(post.tags.all())
# Output: <QuerySet [<Tag: Python>, <Tag: Django>]>

```

---

## Exercise 4: Enhancing the Admin Panel with Tag Filters

**Objective:** Customize the Django admin interface to allow administrators to filter blog posts by their associated tags.

**Instructions:**
1. Open your `blog/admin.py` file.
2. Instead of just registering the model directly, create a new class called `PostAdmin` that inherits from `admin.ModelAdmin`.
3. Inside this class, define a `list_filter` attribute. Set it to a tuple or list containing the string `'tags'`.
4. Update your registration code so that it registers both the `Post` model and your new `PostAdmin` class together. 
5. Start your development server (`python manage.py runserver`), log into the admin panel (`http://127.0.0.1:8000/admin/`), and navigate to the Posts section to see your new filtering sidebar.

<details>
<summary><strong>View Solution & Explanation</strong></summary>

**Update `blog/admin.py`:**
```python
from django.contrib import admin
from .models import Post, Tag

# Ensure the Tag model is also registered so you can manage tags directly!
admin.site.register(Tag)

# Create the custom ModelAdmin class
class PostAdmin(admin.ModelAdmin):
    # This automatically generates a sidebar filter for the ManyToMany field
    list_filter = ('tags',)
    
    # Optional bonus: This makes the main list view look much cleaner
    list_display = ('title', 'author', 'date_posted')

# Register the Post model alongside your custom PostAdmin configuration
admin.site.register(Post, PostAdmin)