from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Player(models.Model):
	belongsTo = models.ForeignKey(User,on_delete = models.CASCADE)
	name = models.CharField(max_length = 10)
	number = models.IntegerField()


	def __str__(self):
		return f"Name: {self.name}, Number {self.number}"
	
