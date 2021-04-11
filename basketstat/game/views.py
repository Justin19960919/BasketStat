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

# self-defined class
from .playerStat import MyPlayerRecord, MyPlayerStat

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
    # change this out later since we have new fields called total score
    our_totalscore = foundGame.quarter1_score + \
                     foundGame.quarter2_score + \
                     foundGame.quarter3_score + \
                     foundGame.quarter4_score
    other_totalscore = foundGame.other_quarter1_score + \
                     foundGame.other_quarter2_score + \
                     foundGame.other_quarter3_score + \
                     foundGame.other_quarter4_score

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


def deleteComment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    cur_gameId = comment.gameId.id
    comment.delete()
    print("Deleted Comment!")
    return HttpResponseRedirect(f'/game/list/{cur_gameId}')


def recordGame(request, id):

    game = Game.objects.get(id=id)
    # POST request
    if request.method == "POST":
        post_results = request.POST
        print("Post request: ", post_results)
        record_id = None
        found_player_record = None

        for k in post_results:
            if post_results[k] == "select-player":
                record_id = int(k)
                break
        
        if record_id:
            found_player_record = PlayerRecord.objects.get(id=record_id)
        
            if "make-2pt" in post_results:
                found_player_record.twoPointersMade += 1
                found_player_record.twoPointers += 1
                game.total_score += 2



            elif "miss-2pt" in post_results:
                found_player_record.twoPointers += 1

            
            elif "make-3pt" in post_results:
                found_player_record.threePointersMade += 1
                found_player_record.threePointers += 1
                game.total_score += 3       


            elif "miss-3pt" in post_results:
                found_player_record.threePointers += 1

            
            elif "make-ft" in post_results:
                found_player_record.freethrowMade += 1
                found_player_record.freethrows += 1
                game.total_score += 1


            elif "miss-ft" in post_results:
                found_player_record.freethrows += 1


            elif "off-reb" in post_results:
                found_player_record.offensiveRebound += 1


            elif "def-reb" in post_results:
                found_player_record.defensiveRebound += 1


            elif "steal" in post_results:
                found_player_record.steal += 1
    

            elif "block" in post_results:
                found_player_record.block += 1


            elif "ast" in post_results:
                found_player_record.assist += 1


            elif "to" in post_results:
                found_player_record.turnover += 1


            elif "off-foul" in post_results:
                found_player_record.offensiveFoul += 1
            

            elif "def-foul" in post_results:
                found_player_record.defensiveFoul += 1
        
            else:
                print("Not found")

            found_player_record.save()
            game.save()
            print("Update of game and players saved")
            messages.success(request, f"{found_player_record.playerId.name} stats updated!")
            

        if "other_team_score2" in post_results:
                game.other_total_score += 2
                game.save()
            
        elif "other_team_score3" in post_results:
                game.other_total_score += 3
                game.save()

    playerRecords = PlayerRecord.objects.filter(gameId=game)
    if game.creator != request.user:
        raise PermissionDenied
    # 403 forbidden




    info = {
        'player_records': playerRecords,
        'game': game,
    }
    return render(request, 'game/game_record.html', info)




class StatView(LoginRequiredMixin, View):

    def get(self,request,id):

        game = Game.objects.get(id=id)
        player_records = PlayerRecord.objects.filter(gameId=game)
        
        player_stats = []
        for pr in player_records:
            pr_object = MyPlayerRecord(
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

            player_stats.append(MyPlayerStat(pr_object).autoGenerate())

        info = {
            'stats': player_stats
        }

        return render(request, 'game/game_stat.html', info)    

    def post(self, request):
        pass









