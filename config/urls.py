from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path

from rest_framework_swagger.views import get_swagger_view

from django.conf import settings

from e_logs.common.all_journals_app.views import get_shifts, get_table_template
from e_logs.common.constructor_app.views import constructor_proxy

handler403 = "e_logs.common.all_journals_app.views.permission_denied"

schema_view = get_swagger_view(title='E-LOGS API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/common/messages/', include('e_logs.common.messages_app.urls')),
    path('api/feedback/', include('e_logs.common.feedback_app.urls')),
    path('api/dashboard/', include('e_logs.common.data_visualization_app.urls')),

    path('api/auth/', include('djoser.urls.base')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/', include('e_logs.common.all_journals_app.api.urls')),
    path('api/', include('e_logs.common.messages_app.api.urls')),
    path('api/bl/', include('e_logs.business_logic.modes.urls')),
    path('api/bl/', include('e_logs.business_logic.blank_shifts.urls')),
    path('api/bl/dicts', include('e_logs.business_logic.dictionaries.urls')),
    path('api/templates/tables/<str:plant_name>/<str:journal_name>/<str:table_name>/',
         get_table_template),
    path('api/constructor/', include('e_logs.common.constructor_app.urls')),
    path('api/<str:plant_name>/<str:journal_name>/get_shifts/', get_shifts),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      re_path(r'^__debug__/', include(debug_toolbar.urls)),
                      re_path(r'^hijack/', include('hijack.urls', namespace='hijack')),
                  ] + urlpatterns
