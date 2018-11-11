from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('get_dicts/', DictionariesApi.as_view()),
    path('autocomplete/', AutocompleteAPI.as_view(), name="Фамилия И.О."),
    path('usernames/', UsernamesAPI.as_view(), name="Имена пользователей"),
    path('concentrates/', ConcentratesAPI.as_view(), name="Концентраты"),
    path('equipment/', EquipmentAPI.as_view(), name="Оборудование"),
    path('emails/', EmailsAPI.as_view(), name="Электронные почты"),


]
