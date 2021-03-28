from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# Create your views here.

# import models
from .models import Game, Comments

# import User
from django.contrib.auth.models import User


# Login required for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Generic Views
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)




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
        'comments': relatedComments,
        'our_totalscore': our_totalscore,
        'other_totalscore': other_totalscore

    }

    #print(info)
    return render(request, 'game/game_detail.html', info)



# create view
class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['season', 'opponent', 'area', 'dateOfGame', 
              'nameOfGame', 'gameUrl']

    # override the form_valid function
    def form_valid(self, form):
        # set the instance to current logged in user
        form.instance.creator = self.request.user
        return super().form_valid(form)



class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    fields = ['season', 'dateOfGame', 'nameOfGame', 'opponent', 'area',
              'other_quarter1_score', 'other_quarter2_score', 'other_quarter3_score',
              'other_quarter4_score', 'gameUrl']

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
    print(comment)
    comment.delete()
    print("Deleted Comment!")
    return HttpResponseRedirect(f'/game/list/{cur_gameId}')

















