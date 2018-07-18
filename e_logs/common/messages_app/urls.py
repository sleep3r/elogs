from django.conf.urls import url
from django.urls import path, re_path
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie
from django.contrib.auth.decorators import login_required


from e_logs.common.messages_app import views

urlpatterns = [
    path('<str:crud>/<str:type>/', process_json_view(auth_required=False)(views.MessageView.as_view()), name='messages'),
    path('get/', process_json_view(auth_required=False)(views.MessageView.as_view()), name='messages_get'),
    path('read/', process_json_view(auth_required=False)(views.MessageView.as_view()), {'crud': 'read'}, name='messages_read'),
    path('list/', login_required(views.MessagesList.as_view()), name='messages_list'),

]
