from django.urls import path

from .views import *

urlpatterns = [
    path('plants/', PlantAPI.as_view()),
    path('journals/', JournalAPI.as_view()),
    path('tables/', TableAPI.as_view()),
    path('fields/', FieldAPI.as_view()),
    path('shifts/<int:id>', ShiftAPI.as_view()),
    path('menu_info/', MenuInfoAPI.as_view()),
    path('settings/', SettingsAPI.as_view()),

]
