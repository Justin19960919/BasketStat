from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse
from django.core.exceptions import ValidationError




class Game(models.Model):
    
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    # player

    nameOfGame = models.CharField(max_length = 20)
    season = models.CharField(max_length = 10)
    dateOfGame =  models.DateTimeField(default = timezone.now)   
    opponent = models.CharField(max_length = 20)
    area = models.CharField(max_length=20)
    gameUrl = models.URLField(blank=True)

    ######## Scores ########
    # score of our team
    quarter1_score = models.IntegerField(default=0)
    quarter2_score = models.IntegerField(default=0)
    quarter3_score = models.IntegerField(default=0)
    quarter4_score = models.IntegerField(default=0)
    # score of the other team
    other_quarter1_score = models.IntegerField(default=0)
    other_quarter2_score = models.IntegerField(default=0)
    other_quarter3_score = models.IntegerField(default=0)
    other_quarter4_score = models.IntegerField(default=0)


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

    # Clean function will automatically fire away, and save the
    # changes made to the model fields
    # def clean(self):
    #     url = self.gameUrl.split("v=")
    #     if len(url) != 2:
    #         raise ValidationError("Game url is not a valid url")
    #     self.gameUrl = url[1]
    #     print(url)
    #     print(len(url))
    #     print(self.gameUrl)





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

