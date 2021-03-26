from django.urls import path

from .views import (UserPostListView, 
					PostCreateView, 
					PostDetailView,
					PostUpdateView,
					PostDeleteView)


urlpatterns = [
	path('', UserPostListView.as_view(), name = 'post-list'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('create/', PostCreateView.as_view(), name = 'post-create'),
	
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'), # update
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'), # delete
]

