from django.urls import path
from . import views

urlpatterns = [
	path('', views.player_list, name = "player-list"),
	path('post_player/', views.postPlayer, name = "post-player"),


]


