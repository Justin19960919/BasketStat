from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.


class Game(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    # Additional information
    season = models.CharField(max_length = 10)
    opponent = models.CharField(max_length = 20)
    area = models.CharField(max_length=20)
    dateOfGame =  models.DateTimeField(default = timezone.now)
    # name of game
    nameOfGame = models.CharField(max_length = 20)
    # additional upload of url from youtube
    gameUrl = models.URLField(blank=True) # default: 200 chars
    
    def __str__(self):
        return f"Creator: {self.creator.username},\
                 Season: {self.season}, \
                 Opponent: {self.opponent}, \
                 Area: {self.area}, \
                 Date of Game: {self.dateOfGame}, \
                 Name of Game: {self.nameOfGame}, \
                 Game URL: {self.gameUrl}.."

    # reverse
    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'id': self.pk})



class Comments(models.Model):
    gameId = models.ForeignKey('Game', on_delete = models.CASCADE)  # foreign key to point to the game

    author = models.CharField(default="Put Author here",
        max_length = 10)
    
    date = models.DateTimeField(default = timezone.now)
    

    comment = models.TextField(default = "Put Content here",
        max_length = 1000)


    def __str__(self):
        return f"gameID: {self.gameId.id}\
                 author: {self.author}\
                 date: {self.date}\
                 comment: {self.comment}."

