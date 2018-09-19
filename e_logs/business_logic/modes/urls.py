from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('modes/', ModeView.as_view()),
    path('modes_api/', ModeApi.as_view()),
]
