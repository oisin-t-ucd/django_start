from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    Stores a single blog post entry related to :model:`auth.User`.
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )
    subtitle = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post {self.title} by {self.author}"

    def save(self, *args, **kwargs):
        # Only auto-generate if the slug is empty
        if not self.slug:
            self.slug = slugify(self.title)

        # Call the parent class's save method
        super().save(*args, **kwargs)


class Comment(models.Model):
    # The ForeignKey ties each comment to a specific Post.
    # 'related_name' is how we will access comments from the Post side.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_comments"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
