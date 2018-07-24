"""DigitalLogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from config.settings import settings
from e_logs.furnace.fractional_app import views
from e_logs.common.all_journals_app.services import shifts
from e_logs.common.all_journals_app.views import JournalView, ShihtaJournalView, MetalsJournalView

handler403 = "e_logs.common.all_journals_app.views.permission_denied"

urlpatterns = [
    url('^$', views.Index.as_view()),
    path('admin/', admin.site.urls),
    url('^auth', include('e_logs.common.login_app.urls')),
    url('^common', include('e_logs.common.all_journals_app.urls')),
    path('common/messages/', include('e_logs.common.messages_app.urls')),
    url('furnace/fractional', include('e_logs.furnace.fractional_app.urls')),
    url('^(?P<plant>furnace)/(?P<journal_name>metals_compute)$', MetalsJournalView.as_view()),
    url('^(?P<plant>furnace)/(?P<journal_name>report_income_outcome_schieht)$', ShihtaJournalView.as_view()),
    url('^(?P<plant>[\w]+)/(?P<journal_name>[\w]+)$', JournalView.as_view()),
    url(r'^(?P<plant>[\w]+)/(?P<journal_name>[\w]+)/get_shifts/$', shifts.get_shifts),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
