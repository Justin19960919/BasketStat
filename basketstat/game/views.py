'''
Django ORM queries
https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html

from django.db.models import Sum
from django.db.models import Avg

// Aggregate 

1. Sum
City.objects.aggregate(Sum('population'))
{'population__sum': 970880224}  # 970,880,224

2. Avg
City.objects.aggregate(Avg('population'))
{'population__avg': 11558097.904761905}  # 11,558,097.90

3. Annotate (Group by) + order by
// task: get population sum by country
.value(col1, col2) // columns to be grouped

City.objects.values('country__name') \
  .annotate(country_population=Sum('population')) \
  .order_by('-country_population')

--Return:
[
  {'country__name': u'China', 'country_population': 309898600},
  {'country__name': u'United States', 'country_population': 102537091},
  {'country__name': u'India', 'country_population': 100350602},
  {'country__name': u'Japan', 'country_population': 65372000},
  {'country__name': u'Brazil', 'country_population': 38676123},
  '...(remaining elements truncated)...'
]

4. filter
City.objects.values('country__name') \
  .annotate(country_population=Sum('population')) \
  .filter(country_population__gt=50000000) \
  .order_by('-country_population')

'''



######################################################################
# CBV tutorial
# https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html

# Many to many relationships
#https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/


# create view
# class GameCreateView(LoginRequiredMixin, CreateView):
#     model = Game
#     form_class = CreateGameForm
#     template_name = "game/game_form.html"

#     # form_valid foes the form saving
#     # override the form_valid function
#     def form_valid(self, form):
#         # set the instance to current logged in user
#         form.instance.creator = self.request.user
#         return super().form_valid(form)
    
    # Constructs a dictionary with the parameters necessary to initialize the form
    # specifies before initialization of form
    # def get_form_kwargs(self):
    #     data = super(GameCreateView, self).get_form_kwargs()
    #     data.update(
    #         players = Player.objects.get(belongsTo=self.request.user)
    #     )
    #     return data

######################################################################

# HTTP
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

# import models
from django.forms.models import modelform_factory
from .models import Game, Comments, PlayerRecord
from player.models import Player


# ORM queries
from django.db.models import Sum, Avg

# Chart js
from django.http import JsonResponse
from django.core import serializers

# import forms
from django import forms
from .forms import CreateGameForm   # self defined form

# contrib
from django.contrib.auth.models import User   # import user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Generic Views
from django.views.generic import (ListView, 
                                  DetailView, 
                                  UpdateView,
                                  DeleteView)
# Class based views
from django.views import View

# My classes
from .playerStat import PlayerGameRecord
from .team import TeamGameRecord


# Other python packages
import datetime
import os
import itertools




# List view
class GameListView(LoginRequiredMixin, ListView):
    model = Game
    context_object_name = 'games'
    
    def get_queryset(self):
        user = self.request.user
        return Game.objects.filter(creator=user).order_by('-dateOfGame')



# Detail view turned to function based view
# display comments and game at the same time in detail view
# id is a parameter here passed in through the url
@login_required
def displayGameAndComment(request, id):
    foundGame = Game.objects.get(id=id)    # get the id of the this game
    players = foundGame.players.all() # get all players associated with this game
    
    allPlayerRecords = []
    for player in players:
        try:
            hit = PlayerRecord.objects.get(playerId=player, gameId=foundGame)
            allPlayerRecords.append(hit)
        except:
            print("No match for the player and game, creating one.. ")
            newPlayerRecord = PlayerRecord(playerId = player, gameId = foundGame)
            newPlayerRecord.save()
            allPlayerRecords.append(newPlayerRecord)

    # use Django Fk set
    relatedComments = foundGame.comments_set.all()
    info = {
        'game': foundGame,
        'player_records':allPlayerRecords,
        'comments': relatedComments,
    }

    return render(request, 'game/game_detail.html', info)



def leaveComment(request, id):
    if request.is_ajax and request.method == "POST":
        gameId = Game.objects.get(id=id)
        comment = request.POST.get('comment')
        author = request.POST.get('author')
        
        newComment = Comments(gameId = gameId,
                              author = author,
                              comment = comment)
        newComment.save()
        print("Saved new comment")
        data = {
            "date": newComment.date,
            "author": author,
            "comment": comment
        }

        return JsonResponse(data)



def deleteComment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    cur_gameId = comment.gameId.id
    comment.delete()
    print("Deleted Comment!")
    return HttpResponseRedirect(f'/game/list/{cur_gameId}')





@login_required
def createGame(request):
    if request.method == "POST":
        form = CreateGameForm(request.user, request.POST)
        if form.is_valid():
            game = form.save(commit = False)
            game.creator = request.user
            game.save()
            # when saving many to many fields, we need to add form.save_m2m()
            form.save_m2m()

            # figure out how to create playerRecord and save in db
            # print('cleaned data: ', form.cleaned_data)
            # get all players in the many to many field
            ################################################
            game_players = form.cleaned_data.get('players')
            for player in game_players:
                print("Creating a new player record for the player:")
                print(player)
                newPlayerRecord = PlayerRecord(
                    playerId=player,
                    gameId=game)
                newPlayerRecord.save()
            ################################################

            return redirect('game-list')
    
    else:
        form = CreateGameForm(request.user)
    

    return render(request, 'game/game_form.html',{'form': form})


# https://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget/27322032
class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    fields = ['players','season', 'dateOfGame', 'nameOfGame', 'opponent', 'area','quarter1_score',
              'quarter2_score', 'quarter3_score','quarter4_score',
              'other_quarter1_score', 'other_quarter2_score', 'other_quarter3_score',
              'other_quarter4_score', 'gameUrl']
    
    # changing the default widgets in selecting multiple fields
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['players'].widget = forms.CheckboxSelectMultiple()
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        game = self.get_object()
        if self.request.user == game.creator:
            return True
        return False


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    success_url = '/game/list'

    def test_func(self):
        game = self.get_object()
        if self.request.user == game.creator:
            return True
        return False





class ProcessGameRecordView(LoginRequiredMixin, View):
    
    quarter = None

    # post request
    def post(self, request, id):
        self.request = request
        self.post_request = request.POST
        self.logging_path = f"game/logs/game_{id}_log.txt"
        self.id = id
        self.game = Game.objects.get(id=id)
        self.processHomeTeam()
        quarter = self.getQuarter()
        print("Quarter: (from POST)", quarter)
        if quarter:
            self.quarter = quarter
        return self.get(request, id)

    # get request
    def get(self, request, id):
        game = Game.objects.get(id=id)
        pr_get = PlayerRecord.objects.filter(gameId=game)
        packet = {
            'player_records': pr_get,
            'game' : game
        }
        if self.quarter:
            packet['quarter'] = self.quarter

        return render(request, 'game/game_record.html', packet)

    
    def getGame(self):
        return self.game


    def getQuarter(self):
        return self.quarter

    def checkOpponentPress(self):
        op_ts1 =  "other_team_score1" in self.post_request
        op_ts2 =  "other_team_score2" in self.post_request
        op_ts3 =  "other_team_score3" in self.post_request
        if op_ts1 or op_ts2 or op_ts3:
            return True
        return False

    def writeToLog(self, msg):
        with open(self.logging_path, 'a') as file:
            msg_time = datetime.datetime.now()
            msg_time = msg_time.strftime("%m/%d/%Y, %H:%M:%S")
            file.write(f"[{msg_time}]   {msg}\n")

    def checkSelectPlayer(self):
        if 'select-player' not in self.post_request:
            return False

        self.player_record_id = self.post_request.get('select-player')
        print('Player record id: ', self.player_record_id)
        return True

    def checkQuarter(self):
        if 'quarter' not in self.post_request:
            return False

        self.quarter = self.post_request.get('quarter')
        print('Quarter: ', self.quarter)
        return True


    def instantiatePlayerRecordObject(self):
        playerRecord = PlayerRecord.objects.get(id = self.player_record_id)
        self.playerRecord = playerRecord
        self.playerName = playerRecord.playerId.name
        self.playerNumber = playerRecord.playerId.number


    def savePlayerRecordAndGame(self):
        self.game.save()
        self.playerRecord.save()



    def createMessageHeader(self):
        if self.quarter and self.playerName and self.playerNumber:
            msg_header = f"{self.quarter.upper()} #{self.playerNumber}|{self.playerName} "
            self.msg_header = msg_header


    def addQuarterScore(self, addPoints):
        if self.game:
            self.game.total_score += addPoints
            if self.quarter == 'q1':
                self.game.quarter1_score += addPoints
                print(f"Added {addPoints} to q1")
            
            elif self.quarter == 'q2':
                self.game.quarter2_score += addPoints
                print(f"Added {addPoints} to q2")

            elif self.quarter == 'q3':
                self.game.quarter3_score += addPoints
                print(f"Added {addPoints} to q3")
            
            elif self.quarter == 'q4':
                self.game.quarter4_score += addPoints
                print(f"Added {addPoints} to q4")

    def addOpponentQuarterScore(self, addPoints):
        if self.game and self.quarter:
            msg = f"{self.quarter.upper()} Opponent make {addPoints}"

            self.game.other_total_score += addPoints
            if self.quarter == 'q1':
                self.game.other_quarter1_score += addPoints
            
            elif self.quarter == 'q2':
                self.game.other_quarter2_score += addPoints

            elif self.quarter == 'q3':
                self.game.other_quarter3_score += addPoints
            
            elif self.quarter == 'q4':
                self.game.other_quarter4_score += addPoints

            print(msg)
            self.game.save()
            self.writeToLog(msg)
            messages.success(self.request, msg)


    def endingSequence(self, additionalMsg):
        print("Saving player record and game record")
        self.savePlayerRecordAndGame()
        print("Creating logging message")
        msg = self.msg_header + additionalMsg
        print("Writing to game logger")
        self.writeToLog(msg)
        print("Finished.. ")
        print("Render msg..")
        messages.success(self.request, msg)


    def make2pt(self):
        if "make-2pt" in self.post_request:
            self.playerRecord.twoPointersMade += 1
            self.playerRecord.twoPointers += 1
            self.addQuarterScore(2)
            self.endingSequence('make 2')


    def miss2pt(self):
        if "miss-2pt" in self.post_request:
            self.playerRecord.twoPointers += 1
            self.endingSequence('miss 2')


    def make3pt(self):
        if "make-3pt" in self.post_request:
            self.playerRecord.threePointersMade += 1
            self.playerRecord.threePointers += 1    
            self.addQuarterScore(3)
            self.endingSequence('make 3')
    

    def miss3pt(self):
        if "miss-3pt" in self.post_request:
            self.playerRecord.threePointers += 1
            msg = self.msg_header + "miss 3"
            self.endingSequence('miss 3')


    def makeft(self):
        if "make-ft" in self.post_request:
            self.playerRecord.freethrowMade += 1
            self.playerRecord.freethrows += 1
            self.addQuarterScore(1)
            self.endingSequence('make ft')


    def missft(self):
        if "miss-ft" in self.post_request:
            self.playerRecord.freethrows += 1
            self.endingSequence('miss ft')
       

    def offReb(self):
        if "off-reb" in self.post_request:
            self.playerRecord.offensiveRebound += 1
            self.endingSequence('get offReb')



    def defReb(self):
        if "def-reb" in self.post_request:
            self.playerRecord.defensiveRebound += 1
            self.endingSequence('get defReb')  


    def steal(self):
        if "steal" in self.post_request:
            self.playerRecord.steal += 1
            self.endingSequence('get steal') 


    def block(self):
        if "block" in self.post_request:
            self.playerRecord.block += 1
            self.endingSequence('get block')             

    def ast(self):
        if "ast" in self.post_request:
            self.playerRecord.assist += 1
            self.endingSequence('get AST') 

    def to(self):
        if "to" in self.post_request:
            self.playerRecord.turnover += 1
            self.endingSequence('has TO') 


    def offFoul(self):
        if "off-foul" in self.post_request:
            self.playerRecord.offensiveFoul += 1
            self.endingSequence('commits OF') 

    def defFoul(self):
        if "def-foul" in self.post_request:
            self.playerRecord.defensiveFoul += 1
            self.endingSequence('commits DF') 

    def determineAction(self):
        self.make2pt()
        self.miss2pt()
        self.make3pt()
        self.miss3pt()
        self.makeft()
        self.missft()
        self.offReb()
        self.defReb()
        self.steal()
        self.block()
        self.ast()
        self.to()
        self.offFoul()
        self.defFoul()


    # access point
    def processHomeTeam(self):
        sp = self.checkSelectPlayer()
        q = self.checkQuarter()
        
        if sp and q:
            # if both are true then we process
            self.instantiatePlayerRecordObject()
            self.createMessageHeader()
            self.determineAction()

        elif not sp and not self.checkOpponentPress():
            messages.warning(self.request, "Need to select a player")
        
        elif not q and not self.checkOpponentPress():
            messages.warning(self.request, "Need to select a quarter")

        # opponent pressed
        else:
            self.processOpponent()


    def processOpponent(self):
        # first check quarter
        if not self.checkQuarter():
            messages.warning(self.request, "Need to select a quarter")
        else:
            addPoints = 0
            # selected quarter
            if 'other_team_score1' in self.post_request:
                addPoints = 1
            elif 'other_team_score2' in self.post_request:
                addPoints = 2
            elif 'other_team_score3' in self.post_request:
                addPoints = 3

            self.addOpponentQuarterScore(addPoints)



############################

class StatView(LoginRequiredMixin, View):

    def get(self,request,id):
        game = Game.objects.get(id=id)
        player_records = PlayerRecord.objects.filter(gameId=game)
        
        player_stats = []
        for pr in player_records:
            pr_object = PlayerGameRecord(
                pr.playerId.name,
                pr.playerId.number,
                pr.numberOfMinutesPlayed,
                pr.twoPointers,
                pr.twoPointersMade,
                pr.threePointers,
                pr.threePointersMade,
                pr.freethrows,
                pr.freethrowMade,
                pr.offensiveRebound,
                pr.defensiveRebound,
                pr.block,
                pr.steal,
                pr.assist,
                pr.turnover,
                pr.offensiveFoul,
                pr.defensiveFoul
                )

            player_stats.append(pr_object.autoGenerate())

        
        info = {
            'id': id,
            'stats': player_stats
        }
        
        return render(request, 'game/game_stat.html', info)    


def get_accumulative(target_list):
    accumulative_list = list(itertools.accumulate(target_list, lambda a,b : a+ b))
    return accumulative_list


def linechart(request, id):
    # test for game 28
    game = Game.objects.get(id=id)
    game_quarter_scores = get_accumulative([game.quarter1_score, game.quarter2_score, game.quarter3_score, game.quarter4_score])
    game_other_quarter_scores = get_accumulative([game.other_quarter1_score, game.other_quarter2_score, game.other_quarter3_score, game.other_quarter4_score])

    print("Home team: ", game_quarter_scores)  # done
    print("Opponent: ", game_other_quarter_scores)    # done

    labels = ['Quarter 1','Quarter 2','Quarter 3','Quarter 4']

    data = {
        'labels':labels,
        'data': [game_quarter_scores, game_other_quarter_scores]
    }

    return JsonResponse(data)



def getTeamStats(request, id):
    tgr = TeamGameRecord()
    game = Game.objects.get(id=id)
    player_records = PlayerRecord.objects.filter(gameId=game)

    # set up the team game record class   
    for pr in player_records:
        tgr.addPlayerRecord(pr)
    
    # initialize all team stats
    tgr.initTeamStat() 

    data = {
        "data": tgr.teamStats,
    }

    return JsonResponse(data)


# chart.js
# 1
# https://www.ordinarycoders.com/blog/article/11-chart-js-examples

# 2
# load charts to the same page
# https://testdriven.io/blog/django-charts/

# def charts(request):
#     return render(request, "game/game_chart.html")




