from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('get_dicts/', DictionariesApi.as_view()),
    path('lastnames/', AutocompleteAPI.as_view(), name="Список фамилий"),
    path('usernames/', UsernamesAPI.as_view(), name="Список пользователей"),
    path('concentrates/', ConcentratesAPI.as_view(), name="Список концентратов"),
    path('equipment/', EquipmentAPI.as_view(), name="Список оборудования"),
    path('emails/', EmailsAPI.as_view(), name="Список электронных почт"),


]
