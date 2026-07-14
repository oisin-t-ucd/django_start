import datetime

from django.utils import timezone

"""
blog/tests.py

These tests evaluate the models and views in the Blog app.

TestCase - is a class provided by Django's test framework used to create our test cases.
Client - is a class that acts as a dummy web browser for simulating GET and POST requests on a URL.
User - is Django’s default user model.
reverse - is a helper function to reverse resolve Django URLs.
Post - is a model class which we are going to test.
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    """
    Defines a new class PostModelTests which is a subclass of TestCase.
    Tests the functionality and methods associated with the Post model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        This class method is called once at the beginning of the test run for class-level setup.
        - cls.user creates a user in the test database.
        - cls.post creates a post in the test database associated with the user we just created.
        """
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.post = Post.objects.create(
            author=cls.user, title="Test Post", content="This is a test post"
        )

    def test_post_content(self):
        """
        Tests the content of the Post created in setUpTestData.
        Retrieves a Post instance by its id and verifies that the author, title,
        and content match what was set up.
        """
        post = Post.objects.get(id=1)
        expected_author = f"{post.author}"
        expected_title = f"{post.title}"
        expected_content = f"{post.content}"
        self.assertEqual(expected_author, "testuser")
        self.assertEqual(expected_title, "Test Post")
        self.assertEqual(expected_content, "This is a test post")

    def test_post_str_method(self):
        """
        Tests the __str__ method of the Post model.
        Ensures that the string representation of a Post instance is the same as the post's title.
        """
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), "Post Test Post by testuser")

    def test_get_absolute_url(self):
        """
        Tests the get_absolute_url method of the Post model.
        Ensures that the URL returned is what is expected by using reverse to generate
        the URL for the 'post-detail' view using the post's id.
        """
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), "/blog/post/1")

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

    def test_is_new_post(self):
        # Create a post dated right now
        recent_post = Post.objects.create(
            author=self.user, title="Recent Post", content="Posted just now."
        )
        self.assertTrue(recent_post.is_new())

        # Create a post dated 3 days ago
        old_time = timezone.now() - datetime.timedelta(days=3)

        old_post = Post.objects.create(
            author=self.user, title="Old Post", content="Posted ages ago."
        )
        # We manually override the auto_now_add date for testing
        old_post.created_on = old_time
        old_post.save()

        self.assertFalse(old_post.is_new())
        old_post = Post.objects.create(
            author=self.user, title="Other Old Post", content="Posted ages ago."
        )
        # We manually override the auto_now_add date for testing
        old_post.created_on = old_time
        old_post.save()

        self.assertFalse(old_post.is_new())


class PostViewsTests(TestCase):
    """
    This class contains tests for the views associated with the Post model.
    """

    def setUp(self):
        """
        Sets up the data needed for the individual tests.
        A Client instance is created to simulate a browser.
        A User and Post instance are created for use in the upcoming tests.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            author=self.user, title="Test Post", content="This is a test post", status=1
        )

    def test_post_list_view(self):
        """
        Tests the view for listing blog posts (home page).
        Simulates a GET request to that URL and checks that the response status is 200 (HTTP OK).
        Checks if the response contains certain text and the correct template is used.
        """
        url = reverse("blog:post_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_post_detail_view(self):
        """
        Tests the view for displaying a single blog post detail.
        Checks the response status and whether the response contains the post's title.
        """
        url = reverse("blog:post_detail", args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_create_post_view(self):
        """
        Checks the post creation view.
        Logs in the test user, checks the GET request, and simulates a POST request
        creating a new post. Verifies a 302 redirect and database creation.
        """
        self.client.login(username="testuser", password="12345")

        # Test GET request
        response = self.client.get(reverse("blog:create_post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

        # Test POST request
        response = self.client.post(
            reverse("blog:create_post"),
            {
                "title": "New title",
                "content": "New text",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Post.objects.filter(title="New title").exists())

    def test_update_post_view(self):
        """
        Checks the post update view.
        Simulates a GET request, then sends a POST request with updated title and content.
        Refreshes the test post instance from the database to check if the title has been updated.
        """
        self.client.login(username="testuser", password="12345")
        url = reverse("blog:update_post", kwargs={"pk": self.post.pk})

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

        # Test POST request
        response = self.client.post(
            url,
            {
                "title": "Updated title",
                "content": "Updated text",
            },
        )
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.post.title, "Updated title")

    def test_delete_post_view(self):
        """
        Verifies the post deletion view.
        Checks the GET request for the confirmation template, then sends a POST request
        to perform the deletion, verifying the post no longer exists.
        """
        self.client.login(username="testuser", password="12345")
        url = reverse("blog:delete_post", kwargs={"pk": self.post.pk})

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_confirm_delete.html")

        # Test POST request
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
