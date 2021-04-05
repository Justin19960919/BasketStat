from django.urls import path
from . import views
from .views import (GameListView, 
					GameUpdateView,
					GameDeleteView)

# /game
urlpatterns = [
	path('list/', GameListView.as_view(), name = 'game-list'),
	path('list/<int:id>',views.displayGameAndComment, name = 'game-detail'),
	# path('create/', GameCreateView.as_view(), name = 'game-create'),
	path('create/', views.createGame, name = 'game-create'),
	# update and delete must be <int:pk>
	path('list/<int:pk>/update/', GameUpdateView.as_view(), name = 'game-update'),
	path('list/<int:pk>/delete/', GameDeleteView.as_view(), name = 'game-delete'),
	path('deleteComment/<int:comment_id>/', views.deleteComment, name="delete-comment"),
]