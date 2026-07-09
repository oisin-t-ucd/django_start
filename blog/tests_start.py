from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    """
    - Defines a new class PostModelTests which is a subclass of TestCase.

    #
    #

    1.  setUpTestData class method
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.post = Post.objects.create(
            author=cls.user, title="Test Post", content="This is a test post"
        )

    def test_post_model_required_fields(self):
        post = Post()
        with self.assertRaises(ValidationError) as context:
            post.full_clean()
        # we didn't provide any of the required fields, so this is the dict of validation errors
        expected_error_dict = {
            "title": ["This field cannot be blank."],
            "slug": ["This field cannot be blank."],
            "subtitle": ["This field cannot be blank."],
            "author": ["This field cannot be null."],
            "content": ["This field cannot be blank."],
        }
        self.assertDictEqual(context.exception.message_dict, expected_error_dict)

    def test_post_model_unique_title(self):
        author = User.objects.get(id=1)
        duplicate_title_post = Post(
            author=author, title="Test Post", content="This is a test post"
        )
        with self.assertRaises(IntegrityError) as context:
            duplicate_title_post.save()
        self.assertIn(
            "UNIQUE constraint failed: blog_post.slug",
            str(context.exception),
        )

    def test_post_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f"{post.author}", "testuser")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post")

    def test_post_str_method(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), "Post Test Post by testuser")

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), "/blog/post/1")


class PostViewsTests(TestCase):
    """
    This class contains tests for the views associated with the Post model.

    5.  setUp method
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            author=self.user, title="Test Post", content="This is a test post", status=1
        )

    def test_post_list_view(self):
        Post.objects.create(
            author=self.user,
            title="Unpublished",
            content="This is a test post",
        )
        Post.objects.create(
            author=self.user,
            title="Deleted",
            content="This is a test post",
            is_deleted=True,
            status=1,
        )
        url = reverse("blog:post_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertNotContains(response, "Unpublished")
        self.assertNotContains(response, "Deleted")
        self.assertTemplateUsed(response, "blog/post_list.html")
