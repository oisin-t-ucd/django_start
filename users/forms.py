from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = ["image", "bio"]  # Added bio to fields

    def clean_image(self):
        image = self.cleaned_data.get("image")

        # Check if an image was actually uploaded
        if image:
            # size is measured in bytes.
            # 2MB = 2 * 1024 * 1024 bytes (2,097,152 bytes)
            max_size = 200 * 1024

            if image.size > max_size:
                raise ValidationError("File too large. Size should not exceed 200KB.")

        return image

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")

        # Check if bio exists before running string methods
        if bio:
            # 1. Check for forbidden word
            forbidden_word = "spam"
            if forbidden_word in bio.lower():
                raise ValidationError(
                    "Please keep your bio professional. Remove forbidden words."
                )

            # 2. Check word count
            word_count = len(bio.split())
            if word_count > 50:
                raise ValidationError(
                    f"Bio is too long! (Current: {word_count} words. Max: 50)"
                )

        return bio


# users/forms.py


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
