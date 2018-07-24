from django.conf.urls import url
from e_logs.common.feedback_app.views import send_message

urlpatterns = [
    url('send-message$', send_message),
]
