from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('plants/', PlantsAPI.as_view()),
    path('journals/', JournalsAPI.as_view()),
    path('tables/', TablesAPI.as_view()),
    path('fields/', FieldsAPI.as_view()),
    path('shifts/', ShiftAPI.as_view()),
    path('shifts/<int:id>', ShiftAPI.as_view()),
    path('menu_info/', MenuInfoAPI.as_view()),
    path('settings/', csrf_exempt(SettingsAPI.as_view())),
    path('autocomplete/', AutocompleteAPI.as_view()),
    path('cell/', CellAPI.as_view()),
]
