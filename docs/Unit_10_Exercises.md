# Django Class-Based Views: Practice Exercises

---

## Exercise 1: The Personal Dashboard (Overriding `get_queryset`)

**Goal:** Understand how `ListView` fetches its data and how to filter it dynamically.

* **The Setup:** Currently, the `PostListView` on your home page displays every post from every user.
* **The Task:** Create a new route (e.g., `/my-posts/`) that uses a `ListView` to display *only* the posts written by the currently logged-in user. You will need to create a new view class, map a new URL, and create a new template (or reuse your existing one).
* **The Challenge:** You cannot simply set `model = Post`, as that will return everything. Instead, you must override the `get_queryset(self)` method in your new view class to filter the `Post` objects by `self.request.user`.

📖 **Docs Reference:** [Generic display views: `ListView` and `get_queryset`](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/#listview)

---

## Exercise 2: The Context Expansion (Overriding `get_context_data`)

**Goal:** Learn how to inject custom, extra variables into a CBV template.

* **The Setup:** On the `PostDetailView`, the template currently displays only the data for that specific post. 
* **The Task:** Add a "Stats Badge" next to the author's name on the detail page that says, "This author has published X total posts."
* **The Challenge:** A `DetailView` automatically passes the single `object` to the template, but nothing else. To pass that `X` (the total count) to the template, you must override the `get_context_data(self, **kwargs)` method inside your `PostDetailView`. Query the database for the author's total post count, add it to the `context` dictionary, and return it.

📖 **Docs Reference:** [Adding extra context to Class-Based Views](https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-display/#adding-extra-context)

---

## Exercise 3: The Search Feature (Handling GET parameters)

**Goal:** Bridge front-end GET requests with back-end ORM filtering within a CBV.

* **The Setup:** Your home page `PostListView` currently shows all posts in descending order of date.
* **The Task:** Add a simple HTML search input box to your navigation bar. The form should use `method="GET"`. If a user searches for the word "Django", the home page's `PostListView` should update to only show posts containing that word.
* **The Challenge:** Modify the `get_queryset` method in your existing `PostListView`. It should check `self.request.GET.get('q')` (assuming your search input has `name="q"`). If a search query exists, filter the queryset by title or content; if not, return all posts as usual.

📖 **Docs Reference:** [Dynamic filtering in generic views](https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-display/#dynamic-filtering)

---

## Exercise 4: The Soft Delete (Overriding `delete`)

**Goal:** Understand the lifecycle of a `DeleteView` and practice defensive database architecture.

* **The Setup:** Currently, your `PostDeleteView` permanently destroys the database record when a user confirms deletion. In many real-world applications, permanently destroying data is risky.
* **The Task:** Implement a "soft delete" system. First, update your `Post` model by adding a boolean field: `is_deleted = models.BooleanField(default=False)`. Run your migrations. Update your `PostListView` so it excludes posts where `is_deleted` is True.
* **The Challenge:** Override the `delete(self, request, *args, **kwargs)` method inside your `PostDeleteView`. Instead of calling the standard delete function to wipe the record, intercept the action: set `self.object.is_deleted = True`, save the object, and return an `HttpResponseRedirect` to your `success_url`.

📖 **Docs Reference:** [Generic editing views: `DeleteView` and `delete()`](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/#deleteview)

---
*Happy Coding! Remember to check the documentation links if you get stuck on the exact syntax for overriding these methods.*
