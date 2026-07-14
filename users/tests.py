from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import Profile

# Create your tests here.
"""
users/tests.py

These tests evaluate the forms and models related to user and profile functionality.

SimpleUploadedFile - class for creating in-memory uploaded file objects to simulate file uploads.
UserRegisterForm, UserUpdateForm, ProfileUpdateForm - local forms for handling user data.
"""


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        Profile.objects.get_or_create(user=self.user, defaults={"image": "default.png"})

    def test_profile_str_method(self):
        # Assuming setUp() already created self.user and self.user.profile
        profile = self.user.profile
        # Assert that str(profile) matches the expected output
        expected_string = "testuser Profile"
        self.assertEqual(str(profile), expected_string)


class UserFormsTests(TestCase):
    """
    Defines a new class UserFormsTests which is a subclass of TestCase.
    Focuses on verifying user registration, updates, and profile constraints.
    """

    def setUp(self):
        """
        Called before every test function is executed.
        Sets up a user and ensures a profile is associated with self.user
        with the default image 'default.png'.
        """
        self.user = User.objects.create_user(username="testuser", password="12345")
        Profile.objects.get_or_create(user=self.user, defaults={"image": "default.png"})

    def test_user_register_form(self):
        """
        Validates the user registration form functionality with valid data.
        If the form is not valid, the test will fail, indicating an issue with validation logic.
        """
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "django1234",
            "password2": "django1234",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_rejects_invalid_email(self):
        """
        Validates the user registration form functionality with valid data.
        If the form is not valid, the test will fail, indicating an issue with validation logic.
        """
        form_data = {
            "username": "newuser",
            "email": "newuser@example",
            "password1": "django1234",
            "password2": "django1234",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(form.errors, {"email": ["Enter a valid email address."]})

    def test_user_update_form(self):
        """
        Verifies the functionality of the user update form.
        Passes new data into UserUpdateForm, validates, saves, and refreshes the database
        to ensure the username has been correctly updated.
        """
        form_data = {"username": "updateduser", "email": "updateduser@example.com"}
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_profile_update_with_invalid_image_format(self):
        """
        Tests profile update functionality when an invalid image file is provided.
        Simulates a user trying to upload a text file where an image is expected.
        The form is expected to be invalid.
        """
        invalid_image_data = b"this is not real image data"
        invalid_image_file = SimpleUploadedFile(
            "new_image.txt", invalid_image_data, content_type="text/plain"
        )

        form = ProfileUpdateForm(
            files={"image": invalid_image_file}, instance=self.user.profile
        )
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "image": [
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
                ]
            },
        )

    def test_profile_update_with_oversized_image(self):
        """
        Assesses the profile update functionality for when an image file exceeds the acceptable size.
        Simulates a 5MB file of null bytes to ensure oversized files are properly rejected.
        """
        oversized_image_data = b"\x00" * 5242880  # 5MB of zeros
        oversized_image_file = SimpleUploadedFile(
            "new_image.jpg", oversized_image_data, content_type="image/jpeg"
        )

        form = ProfileUpdateForm(
            files={"image": oversized_image_file}, instance=self.user.profile
        )
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "image": [
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
                ]
            },
        )
