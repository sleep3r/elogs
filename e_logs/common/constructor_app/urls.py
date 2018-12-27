from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('upload/', csrf_exempt(ConstructorUploadAPI.as_view())),
    path('alter/', csrf_exempt(ConstructorAlterJournalAPI.as_view())),
    path('journal/', csrf_exempt(ConstructorJournalAPI.as_view())),
    path('<str:path>/', constructor_proxy),
]
