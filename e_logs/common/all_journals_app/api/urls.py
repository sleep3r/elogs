from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('plants/', PlantsAPI.as_view()),
    path('journals/', JournalsAPI.as_view()),
    path('tables/', TablesAPI.as_view()),
    path('fields/', FieldsAPI.as_view()),
    path('shifts/', GroupAPI.as_view()),
    path('last_shifts/', LastShiftsIDs.as_view()),
    path('shifts/<int:id>', GroupAPI.as_view()),
    path('menu_info/', MenuInfoAPI.as_view()),
    path('settings/', csrf_exempt(SettingsAPI.as_view())),
    path('setting/', csrf_exempt(SettingAPI.as_view())),
    path('cell/', CellAPI.as_view()),
    path('field/', FieldAPI.as_view()),
    path('scheme/', SchemeAPI.as_view()),
]
