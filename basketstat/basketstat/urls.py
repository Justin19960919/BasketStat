"""basketstat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
# Built in auth views for login, logout functionality
from django.contrib.auth import views as auth_views 

from django.urls import path, include   #include used in line 51 from django.conf import settings 


# Import app views
from usrs import views as usr_views
# ex:
# from posts import views as post_views


#  To add media root (suitable for development)
#from django.conf.urls.static import static 
#from django.conf import settings



urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # players
    path('players/',include('player.urls')),

    # game
    path('game/', include('game.urls')),
    
    # posts app
    path('posts/', include('posts.urls')),
    
    # home app
    path('', include('home.urls')),
    
    # my app (example for ajax)
    path('example/', include('my_app.urls')),

    # user register, login, logout views
    path('register/', usr_views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='usrs/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='usrs/logout.html'), name='logout'),
]




