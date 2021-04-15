from django.urls import path
from my_app.views import (
    indexView,
    postFriend,
    checkNickName,
    test
)

urlpatterns = [
    path('', indexView),
    path('post/ajax/friend', postFriend, name = "post_friend"),
 	path('get/ajax/validate/nickname', checkNickName, name = "validate_nickname"),
 	path('test/', test, name='test'),
]