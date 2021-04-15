from django.db.models.signals import post_save	# signal that gets fired after post is saved
from django.contrib.auth.models import User 	# import built in user model (Sender)
from django.dispatch import receiver			# Receiver gets signal and performs tasks 
from .models import Profile  					# import profile model

# This is taught in Part 8 of Corey's django series
# Creates the profile using signals.py, when user registers an account.


#@receiver is imported

# run everytime an user is created
# when a user is saved, send signal: post_save, and is received by create_profile

# instance: instance of the User
# created: Create an object with the instance of the user that was created

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Takes 	signal and sender
# When user is saved, send signal to receiver, which is the save_profile function
# 
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# Import signals into apps.py

