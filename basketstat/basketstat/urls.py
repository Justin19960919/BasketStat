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

#  To add media root
from django.conf.urls.static import static 
from django.conf import settings

# Import app views
from usrs import views as usr_views





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
    
    ###### PasswordResetView is built in ######
    # pathword reset   
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='usrs/password_reset.html'
         ),
         name='password_reset'),
    
    # when pwd reset is done, render this
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='usrs/password_reset_done.html'
         ),
         name='password_reset_done'),
    

    # form to reset the password
    # uidb64: user id encoded in base 64; token : password token
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usrs/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usrs/password_reset_complete.html'
         ),
         name='password_reset_complete'), 
    ##############################


    # profile
    path('profile/', usr_views.profile, name='profile'),
]

# media route
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




