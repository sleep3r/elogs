from django.urls import path

from .views import *

urlpatterns = [
    path('', SettingsList.as_view()),
]
