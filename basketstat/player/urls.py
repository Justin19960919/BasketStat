from django.urls import path
from . import views

urlpatterns = [
	path('', views.player_list, name = "player-list"),
	path('delete/<int:id>',views.delete_player, name="player-delete")
]


