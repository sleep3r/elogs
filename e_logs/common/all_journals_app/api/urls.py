from django.urls import path

from .views import *

urlpatterns = [
    path('plants/', PlantAPI.as_view()),
    path('journals/', JournalAPI.as_view()),
    path('tables/', TableAPI.as_view()),
    path('fields/', FieldAPI.as_view()),
    path('cells/<int:id>', CellAPI.as_view()),
    path('shifts/<int:id>', ShiftAPI1.as_view()),
    path('menu_info', MenuInfoAPI.as_view()),

    # path('journals/', JournalsList.as_view()),
    # path('tables/', TablesList.as_view()),
    # path('fields/', FieldsList.as_view()),
    # path('cells/', CellsList.as_view()),
    # path('shifts/', ShiftList.as_view()),
]
