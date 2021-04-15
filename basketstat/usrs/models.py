from django.db import models
from django.contrib.auth.models import User
from PIL import Image   # Use Pillow to resize



# Create a profile model (DB), to upload img
class Profile(models.Model):
    # create 1-1 relation
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # default img; upload dir: profile_pics
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'      # USERNAME Profile

    # This save() method already exists, we are overwriting it to resize the image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # open the image instance
        img = Image.open(self.image.path)
        # If img is bigger than 300 * 300
        if img.height > 300 or img.width > 300:
            # resize
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) # save it back

# after this migrates, it will create a dir called profile_pics, with the same level
# as the root dir, to change the location, specify the MEDIA ROOT in settings.py in 
# the project folder



