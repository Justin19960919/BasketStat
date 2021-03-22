from django.urls import path
#import views.py to use the functions defined inside
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('test/', views.test, name='test'),
]
