from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

# import models
from django.forms.models import modelform_factory
from .models import Game, Comments, PlayerRecord
from player.models import Player
# import User
from django.contrib.auth.models import User

# import forms
from django import forms
from .forms import CreateGameForm

# Login required for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Generic Views
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

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
    print(foundGame)
    
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
        'our_totalscore': our_totalscore,
        'other_totalscore': other_totalscore

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

















