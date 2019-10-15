from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from e_logs.common.messages_app.views import MessagesSubscription

urlpatterns = [
    path('subscribe/', csrf_exempt(MessagesSubscription.as_view()), name='messages_sub'),
]
