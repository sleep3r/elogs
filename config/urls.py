from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view

from django.conf import settings
from django.conf.urls import url

from e_logs.common.all_journals_app.views import get_groups, get_table_template
from e_logs.common.constructor_app.views import constructor_proxy

handler403 = "e_logs.common.all_journals_app.views.permission_denied"

schema_view = get_swagger_view(title='E-LOGS API')

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
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
    path('api/bl/dicts/', include('e_logs.business_logic.dictionaries.urls')),
    path('api/templates/tables/', get_table_template),
    path('api/constructor/', include('e_logs.common.constructor_app.urls')),
    path('api/<str:plant_name>/<str:journal_name>/get_groups/', get_groups),
    url(r'furnace.*', TemplateView.as_view(template_name="index.html")),
    url(r'electrolysis.*', TemplateView.as_view(template_name="index.html")),
    url(r'leaching.*', TemplateView.as_view(template_name="index.html")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      re_path(r'^__debug__/', include(debug_toolbar.urls)),
                      re_path(r'^hijack/', include('hijack.urls', namespace='hijack')),
                  ] + urlpatterns
