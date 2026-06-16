from django.contrib.auth.models import User
from django.db import models

STATUS = ((0, "Draft"), (1, "Published"))


class Product(models.Model):
    """
    Stores a single blog post entry related to :model:`auth.User`.
    """

    title = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category")


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
