from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from django.urls import reverse
# Post Model

class Post(models.Model):
	# The account that issued the post
	account = models.ForeignKey(User, on_delete = models.CASCADE)

	author = models.CharField(default="Author",
		max_length = 10)
	
	date = models.DateTimeField(default = timezone.now)
	
	title = models.CharField(default = "Title", max_length = 20)

	content = models.TextField(default = "Content",
		max_length = 1000)



	def __str__(self):
		return f"Author: {self.author}; \
				 Date: {self.date}; \
				 Title: {self.title}; \
				 Content: {self.content}."


    # find location of specific post
    # reverse: return path as string
    # this is handling the PostDetail view <int:pk> in urls.py in the blog app
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})




##### Example models ######
'''
class Game(models.Model):
    title = models.CharField(default="Anonymous Game", max_length = 30)
    gameUrl = models.URLField() # default: 200 chars
    opponent = models.CharField(max_length = 50)
    date =  models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    
    # __str__ method for logging        
    def __str__(self):
        return f"Title: {self.title};\
                Author: {self.author};\
                Opponent: {self.opponent};\
                 Data: {self.date}."

    def get_absolute_url(self):
        return reverse('record-detail', kwargs={'pk': self.pk})


# Create a Profile model with 1-1 relationship with Inbuilt User Model
# After we create the model, make migrations: python manage.py make migrations
# Register at admin.py
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	## Team information
	teamName = models.CharField(max_length=15, default='Unknown Team')
	creationTime = models.DateTimeField(default=timezone.now)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f"{self.user.username} Profile created"

	# This save() method already exists, overwriting it to resize the image
	def save(self):
	    super().save()
	    # open the image instance
	    img = Image.open(self.image.path)
	    # If img is bigger than 300 * 300
	    if img.height > 300 or img.width > 300:
	        # resize
	        output_size = (300, 300)
	        img.thumbnail(output_size)
	        img.save(self.image.path) # save it back


# Specify media root in the settings.py and specify media root 
# and media url to create the profile pics folder inside


'''