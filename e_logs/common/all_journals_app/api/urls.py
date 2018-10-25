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
    path('setting/', csrf_exempt(SettingAPI.as_view())),
    path('autocomplete/', AutocompleteAPI.as_view()),
    path('load_journal/', csrf_exempt(LoadJournalAPI.as_view())),
    path('constructor/hash/', csrf_exempt(ConstructorHashAPI.as_view())),
    path('constructor/upload/', csrf_exempt(ConstructorUploadAPI.as_view())),
    path('cell/', CellAPI.as_view()),
    path('prev-shift/', PrevShiftAPI.as_view()),
]
