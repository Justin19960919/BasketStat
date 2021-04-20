from django.urls import path
from . import views
from .views import (GameListView, 
					GameUpdateView,
					GameDeleteView,
					ProcessGameRecordView,
					StatView)

# /game
urlpatterns = [
	# testing path
	path('test/', views.printTeamStats),
	# charts
	path('test-linechart/', views.linechart, name="linechart"),
	path('charts/', views.charts, name="charts"),

	#####
	path('list/', GameListView.as_view(), name = 'game-list'),
	path('list/<int:id>',views.displayGameAndComment, name = 'game-detail'),
	# path('record/<int:id>',views.recordGame, name = 'game-record'),
	path('record/<int:id>',ProcessGameRecordView.as_view(), name = 'game-record'),
	path('stats/<int:id>', StatView.as_view(), name="game-stat"),

	# path('create/', GameCreateView.as_view(), name = 'game-create'),
	path('create/', views.createGame, name = 'game-create'),
	# update and delete must be <int:pk>
	path('list/<int:pk>/update/', GameUpdateView.as_view(), name = 'game-update'),
	path('list/<int:pk>/delete/', GameDeleteView.as_view(), name = 'game-delete'),
	path('deleteComment/<int:comment_id>/', views.deleteComment, name="delete-comment"),
]