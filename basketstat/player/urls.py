from django.urls import path
from . import views
from .views import DisplayPlayerStats


urlpatterns = [
	path('', views.player_list, name = "player-list"),
	path('delete/<int:id>',views.delete_player, name="player-delete"),
	path('player_stats/<int:player_id>', DisplayPlayerStats.as_view(), name='player-stats'),
]


