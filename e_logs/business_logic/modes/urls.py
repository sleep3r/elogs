from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('create_mode/', create_mode),
    path('modes/', ModeView.as_view()),

]
