from django.urls import path
from . import views
from .views import (GameListView, 
					GameUpdateView,
					GameDeleteView,
					ProcessGameRecordView,
					StatView)

# /game
urlpatterns = [


	#### chart.js routes
	path('shot-selection/<int:id>', views.getTeamStats, name="teamStats"),
	path('quarter-scores/<int:id>', views.linechart, name="linechart"),

	

	#####
	path('list/', GameListView.as_view(), name = 'game-list'),
	path('list/<int:id>',views.displayGameAndComment, name = 'game-detail'),

	path('leaveComment/<int:id>', views.leaveComment, name="leave-comment"),
	path('deleteComment/<int:comment_id>/', views.deleteComment, name="delete-comment"),

	path('record/<int:id>',ProcessGameRecordView.as_view(), name = 'game-record'),
	path('stats/<int:id>', StatView.as_view(), name="game-stat"),


	path('create/', views.createGame, name = 'game-create'),

	# update and delete must be <int:pk>
	path('list/<int:pk>/update/', GameUpdateView.as_view(), name = 'game-update'),
	path('list/<int:pk>/delete/', GameDeleteView.as_view(), name = 'game-delete'),
	
]