from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('modes_api/', csrf_exempt(ModeApi.as_view())),
    path('modes_api/<int:id>', mode_delete),
]
