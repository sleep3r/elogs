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

# from leaching.express_anal_app import views
from DigitalLogs import settings
from furnace.fractional_app import views
from common.all_journals_app.services import shifts

urlpatterns = [
    url('^$', views.index),
    path('admin/', admin.site.urls),
    url('leaching/repair', include('leaching.repair_app.urls')),
    url('^leaching/', include('leaching.express_anal_app.urls')),
    url('^leaching_new/journal', include('leaching.express_analysis_app.urls')),
    url('^leaching_new/repair', include('leaching.repair_reports_app.urls')),
    url('furnace/fractional', include('furnace.fractional_app.urls')),
    url('furnace/concentrate_report_journal', include('furnace.concentrate_report_app.urls')),
    url('furnace/report_income_outcome_schieht', include('furnace.loading_shihta_app.urls')),
    url('furnace/metals_compute', include('furnace.metals_compute_app.urls')),
    url('furnace/technological_tasks', include('furnace.replaceable_technological_tasks_app.urls')),
    url('furnace/furnace_repair', include('furnace.repair_app.urls')),
    url('furnace/furnace_changed_fraction', include('furnace.changed_fraction_app.urls')),
    url('furnace/buff_journal', include('furnace.buffering_app.urls')),
    url('furnace/reports_furnace_area', include('furnace.reports_furnace_area_app.urls')),
    url('electrolysis/electrolysis_technical_report_4_degree', include('electrolysis.technical_report_app4.urls')),
    url('electrolysis/electrolysis_technical_report_3_degree', include('electrolysis.technical_report_app3.urls')),
    url('electrolysis/electrolysis_technical_report_12_degree', include('electrolysis.technical_report_app12.urls')),
    url('electrolysis/electrolysis_repair_report_tables', include('electrolysis.repair_report_app.urls')),
    url('electrolysis/masters_raports', include('electrolysis.masters_raports_app.urls')),
    url('^auth', include('login_app.urls')),
    url('^common', include('common.all_journals_app.urls')),
    url('^common/messages', include('common.messages_app.urls')),
    url(r'^(?P<plant>[\w]+)/(?P<journal_name>[\w]+)/get_shifts/$', shifts.get_shifts),
]
