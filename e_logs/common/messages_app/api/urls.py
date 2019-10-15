from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('messages/', csrf_exempt(MessagesAPI.as_view())),
    path('messages/list', MessagesList.as_view()),

]
