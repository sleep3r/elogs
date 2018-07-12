from django.conf.urls import url
from django.urls import path, re_path
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie


from common.messages_app import views

urlpatterns = [
    re_path(r'get$', process_json_view(auth_required=False)(views.GetMessagesView.as_view()), name='messages_get'),
    re_path(r'read$', process_json_view(auth_required=False)(views.ReadMessagesView.as_view()), name='messages_read'),
    re_path(r'add$', process_json_view(auth_required=False)(views.AddMessagesView.as_view()), name='messages_add'),
    re_path(r'del$', process_json_view(auth_required=False)(views.DelMessagesView.as_view()), name='messages_del'),
    re_path(r'comment$', process_json_view(auth_required=False)(views.AddComment.as_view()), name='messages_comment')
]
