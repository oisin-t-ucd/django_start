from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the default value here corresponds to the file path after manually uploading 'default.jpg' to cloudinary
    # the filename gets an automatic hash (renaming on cloudinary does not change the stored filename)
    # then we need to traverse up 1 level as the file is uploaded to the 'media' folder, not the 'profile_pics' folder
    image = models.ImageField(default="../default_tlhti0.jpg", upload_to="profile_pics")
    bio = models.TextField(blank=True, null=False)  # Added bio field

    def __str__(self):
        return f"{self.user.username} Profile"
