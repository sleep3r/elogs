from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib.auth.decorators import user_passes_test

from rest_framework_swagger.views import get_swagger_view

from django.conf import settings
from e_logs.common.all_journals_app.views import JournalView, get_shifts, Index, get_table_template, get_menu_info

handler403 = "e_logs.common.all_journals_app.views.permission_denied"
schema_view = get_swagger_view(title='E-LOGS API')

urlpatterns = [
    path('', Index.as_view()),
    path('admin/', admin.site.urls),
    path('auth', include('e_logs.common.login_app.urls')),
    path('common', include('e_logs.common.all_journals_app.urls')),
    path('common/messages/', include('e_logs.common.messages_app.urls')),
    path('common/settings/', include('e_logs.common.settings_app.urls')),
    path('feedback/', include('e_logs.common.feedback_app.urls')),
    path('dashboard/', include('e_logs.common.data_visualization_app.urls')),
    path('furnace/fractional', include('e_logs.furnace.fractional_app.urls')),

    re_path(r'^api/auth/', include('djoser.urls.base')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
    re_path(r'^api/auth/', include('djoser.urls.jwt')),
    re_path(r'^api/docs/$', user_passes_test(lambda u: u.is_superuser)(schema_view)),
    re_path(r'^api/', include('e_logs.common.all_journals_app.api.urls')),
    path('bl/', include('e_logs.business_logic.modes.urls')),
    path('bl/', include('e_logs.business_logic.blank_shifts.urls')),
    path('furnace/fractional/', include('e_logs.furnace.fractional_app.urls')),
    path('templates/tables/<str:plant_name>/<str:journal_name>/<str:table_name>/', get_table_template),
    path('<str:plant_name>/<str:journal_name>/', JournalView.as_view()),
    path('<str:plant_name>/<str:journal_name>/<int:page_id>/', JournalView.as_view(),
         name='journal_view'),
    path('<str:plant_name>/<str:journal_name>/get_shifts/', get_shifts),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      re_path(r'^__debug__/', include(debug_toolbar.urls)),
                      re_path(r'^hijack/', include('hijack.urls', namespace='hijack')),
                  ] + urlpatterns
