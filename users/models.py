from django.contrib.auth.models import User
from django.db import models
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"
    
    # Override the built-in save method
    def save(self, *args, **kwargs):
        # 1. Run the default save method first to safely store the file
        super().save(*args, **kwargs)

        # 2. Open the newly saved image using Pillow
        img = Image.open(self.image.path)

        # 3. Check if the image is unnecessarily large
        if img.height > 300 or img.width > 300:
            # 4. Define the maximum allowed dimensions
            output_size = (300, 300)

            # 5. Resize the image (maintaining aspect ratio)
            img.thumbnail(output_size)

            # 6. Overwrite the original large file with the new, optimized version
            img.save(self.image.path)
