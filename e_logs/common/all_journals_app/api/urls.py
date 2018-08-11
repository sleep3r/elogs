from django.urls import path

from .views import *

urlpatterns = [
    path('plants/<str:name>', PlantAPI.as_view()),
    path('journals/<str:name>', JournalAPI.as_view()),
    path('tables/<str:name>', TableAPI.as_view()),
    path('fields/<int:id>', FieldAPI.as_view()),
    path('cells/<int:id>', CellAPI.as_view()),

    path('plants/', PlantsList.as_view()),
    path('journals/', JournalsList.as_view()),
    path('tables/', TablesList.as_view()),
    path('fields/', FieldsList.as_view()),
    path('cells/', CellsList.as_view()),
]
