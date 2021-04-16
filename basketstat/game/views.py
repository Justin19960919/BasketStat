# HTTP
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

# import models
from django.forms.models import modelform_factory
from .models import Game, Comments, PlayerRecord
from player.models import Player


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
from .playerStat import PlayerGameRecord, ProcessGameRecord
from .team import TeamGameRecord

# Other python packages
import datetime
import os

# Logging

# def writeGamelog(path, msg):
#     with open(path, 'a') as file:
#         msg_time = datetime.datetime.now()
#         msg_time = msg_time.strftime("%m/%d/%Y, %H:%M:%S")
#         file.write(f"[{msg_time}]   {msg}\n")


# CBV tutorial
# https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html

# Many to many relationships
#https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/

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
    foundGame = Game.objects.get(id=id)
    # print(foundGame)
    
    # if this is a post request
    if request.method == 'POST':
        if "addComment" in request.POST:
            print("Received post request from adding comments ...")
            print(request.POST)
            # print(request.POST['addComment'])
            # print(request.POST['comment'])
            # print(request.POST['author'])
            print("Starting to fetch comment info..")
            commentInfo = request.POST.get('comment')
            commentAuthor = request.POST.get('author')
            comment_GameId = foundGame

            # create an object of the Comments model
            newComment = Comments(gameId=comment_GameId,
                                  author=commentAuthor,
                                  comment=commentInfo)
            newComment.save()
            print("Saved new comment")

    # query for all the player who played in the game
    players = foundGame.players.all()
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

    print("All player records: ")
    print(allPlayerRecords)

    relatedComments = Comments.objects.filter(gameId=foundGame)

    info = {
        'game': foundGame,
        'players': players,
        'player_records':allPlayerRecords,
        'comments': relatedComments,
    }

    #print(info)
    return render(request, 'game/game_detail.html', info)



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


@login_required
def deleteComment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    cur_gameId = comment.gameId.id
    comment.delete()
    print("Deleted Comment!")
    return HttpResponseRedirect(f'/game/list/{cur_gameId}')


'''
@login_required
def recordGame(request, id):

    game = Game.objects.get(id=id)
    path = f"game/logs/game_{id}_log.txt"
    quarter = None
    # POST request
    if request.method == "POST":
        post_results = request.POST
        print(post_results)     # sanity check
        quarter = None

        if 'select-player' not in post_results:
            msg = "Need to select player"
            messages.warning(request, msg)

        if 'quarter' not in post_results:
            msg = "Need to select quarter"
            messages.warning(request, msg)


        if 'quarter' in post_results and 'select-player' in post_results:
            
            quarter = post_results.get('quarter')
            player_record_id = post_results.get('select-player')
            
            print('Quarter: ', quarter)
            print('Player record id: ', player_record_id)

            found_player_record = PlayerRecord.objects.get(id=player_record_id)
            print("Found player record: ", found_player_record)
            
            name = found_player_record.playerId.name
            number= found_player_record.playerId.number

            if "make-2pt" in post_results:
                found_player_record.twoPointersMade += 1
                found_player_record.twoPointers += 1
                game.total_score += 2
                msg = f"#{number}|{name} make 2"

                if quarter:
                    if quarter == "q1":
                        game.quarter1_score += 2
                    elif quarter == "q2":
                        game.quarter2_score += 2
                    elif quarter == "q3":
                        game.quarter3_score += 2
                    elif quarter == "q4":
                        game.quarter4_score += 2


            elif "miss-2pt" in post_results:
                found_player_record.twoPointers += 1
                msg = f"#{number}|{name} miss 2"
            
            elif "make-3pt" in post_results:
                found_player_record.threePointersMade += 1
                found_player_record.threePointers += 1
                game.total_score += 3       
                msg = f"#{number}|{name} make 3"
                if quarter:
                    if quarter == "q1":
                        game.quarter1_score += 3
                    elif quarter == "q2":
                        game.quarter2_score += 3
                    elif quarter == "q3":
                        game.quarter3_score += 3
                    elif quarter == "q4":
                        game.quarter4_score += 3

            elif "miss-3pt" in post_results:
                found_player_record.threePointers += 1
                msg = f"#{number}|{name} miss 3"

 
            elif "make-ft" in post_results:
                found_player_record.freethrowMade += 1
                found_player_record.freethrows += 1
                game.total_score += 1
                msg = f"#{number}|{name} make ft"

                if quarter:
                    if quarter == "q1":
                        game.quarter1_score += 1
                    elif quarter == "q2":
                        game.quarter2_score += 1
                    elif quarter == "q3":
                        game.quarter3_score += 1
                    elif quarter == "q4":
                        game.quarter4_score += 1


            elif "miss-ft" in post_results:
                found_player_record.freethrows += 1
                msg = f"#{number}|{name} miss ft"

            elif "off-reb" in post_results:
                found_player_record.offensiveRebound += 1
                msg = f"#{number}|{name} get OR"


            elif "def-reb" in post_results:
                found_player_record.defensiveRebound += 1
                msg = f"#{number}|{name} get DR"

            elif "steal" in post_results:
                found_player_record.steal += 1
                msg = f"#{number}|{name} get STL"

            elif "block" in post_results:
                found_player_record.block += 1
                msg = f"#{number}|{name} get BLK"

            elif "ast" in post_results:
                found_player_record.assist += 1
                msg = f"#{number}|{name} get AST"

            elif "to" in post_results:
                found_player_record.turnover += 1
                msg = f"#{number}|{name} has TO"

            elif "off-foul" in post_results:
                found_player_record.offensiveFoul += 1
                msg = f"#{number}|{name} commits OF"

            elif "def-foul" in post_results:
                found_player_record.defensiveFoul += 1
                msg = f"#{number}|{name} commits DF"


            found_player_record.save()
            game.save()
            messages.success(request, msg)
            
            # save to game logger
            print(f"Writing to logger.. {msg}\n")
            writeGamelog(path, msg)

        if 'quarter' in post_results:
            quarter = post_results.get('quarter')
            print(f"Other team {quarter}")
            if "other_team_score1" in post_results:
                print("other team score 1")
                game.other_total_score += 1
                if quarter:
                    if quarter == "q1":
                        game.other_quarter1_score += 1
                    elif quarter == "q2":
                        game.other_quarter2_score += 1
                    elif quarter == "q3":
                        game.other_quarter3_score += 1
                    elif quarter == "q4":
                        print("hit")
                        game.other_quarter4_score += 1
                msg = "Opponent scores 1"
                writeGamelog(path, msg)
                game.save()
                messages.info(request, msg)

            if "other_team_score2" in post_results:
                print("other team score 2")
                game.other_total_score += 2
                if quarter:
                    if quarter == "q1":
                        game.other_quarter1_score += 2
                    elif quarter == "q2":
                        game.other_quarter2_score += 2
                    elif quarter == "q3":
                        game.other_quarter3_score += 2
                    elif quarter == "q4":
                        game.other_quarter4_score += 2
                msg = "Opponent scores 2"
                writeGamelog(path, msg)
                game.save()
                messages.info(request, msg) 
            
            if "other_team_score3" in post_results:
                print("other team score 3")
                game.other_total_score += 3
                print(quarter)
                if quarter:
                    if quarter == "q1":
                        game.other_quarter1_score += 3
                    elif quarter == "q2":
                        game.other_quarter2_score += 3
                    elif quarter == "q3":
                        game.other_quarter3_score += 3
                    elif quarter == "q4":
                        game.other_quarter4_score += 3
                msg = "Opponent scores 3"
                writeGamelog(path, msg)
                game.save()
                messages.info(request, msg)


    # Drop down to get request
    playerRecords = PlayerRecord.objects.filter(gameId=game)
    if game.creator != request.user:
        raise PermissionDenied
        # 403 forbidden


    info = {
        'player_records': playerRecords,
        'game': game,
    }
    if quarter:
        info['quarter'] = quarter
    return render(request, 'game/game_record.html', info)
'''

# strange

@login_required
def recordGame(request, id):
    path = f"game/logs/game_{id}_log.txt"
    if request.method == "POST":
        pgr = ProcessGameRecord(request, path, id)
        # print(pgr.game)
        pgr.processHomeTeam()
        quarter = pgr.getQuarter()


    game = Game.objects.get(id=id)
    quarter = None
    pr_get = PlayerRecord.objects.filter(gameId=game)
    packet = {
        'player_records': pr_get,
        'game' : game
    }

    if quarter:
        packet['quarter'] = quarter
    
    return render(request, 'game/game_record.html', packet)





class StatView(LoginRequiredMixin, View):
    # file downloading
    # https://djangoadventures.com/how-to-create-file-download-links-in-django/
    # render logs (commented it out)
    def openLogger(self, game_id):
        game_path = f"game/logs/game_{game_id}_log.txt"

        if os.path.exists(game_path):
            f = open(game_path, 'r')
            game_log = f.readlines()
            f.close()
            return game_log

        return None

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

        # game_log = self.openLogger(id)
        
        info = {
            'stats': player_stats
        }
        
        # if game_log:
        #     info['logs'] = game_log

        return render(request, 'game/game_stat.html', info)    

    def post(self, request):
        pass


## Using django chartits to render charts on the page

def charts(request):
    return render(request, "game/game_chart.html")

def testing(request):
    # test for game 28
    g28 = Game.objects.get(id=28)
    print(g28)





    return HttpResponse("Testing")

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

























