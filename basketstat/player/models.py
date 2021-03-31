from django.db import models
from game.models import Game
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
	belongsTo = models.ForeignKey(User,on_delete = models.CASCADE)
	name = models.CharField(max_length = 10)
	number = models.IntegerField()

	

# Player records
class PlayerRecord(models.Model):
	
	# point to record
	playerId = models.ForeignKey(Player, on_delete = models.CASCADE)
	gameId = models.ForeignKey(Game, on_delete = models.CASCADE)

	twoPointers = models.IntegerField(default = 0)
	twoPointersMade = models.IntegerField(default = 0)

	threePointers = models.IntegerField(default = 0)
	threePointersMade = models.IntegerField(default = 0)

	freethrows = models.IntegerField(default = 0)
	freethrowMade = models.IntegerField(default = 0)

	offensiveRebound = models.IntegerField(default = 0)
	defensiveRebound = models.IntegerField(default = 0)

	block = models.IntegerField(default = 0)
	steal = models.IntegerField(default = 0)
	assist = models.IntegerField(default = 0)
	turnover = models.IntegerField(default = 0)

	offensiveFoul = models.IntegerField(default = 0)
	defensiveFoul = models.IntegerField(default = 0)

	numberOfMinutesPlayed = models.IntegerField(default = 0)




