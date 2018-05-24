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
from furnace.fractional_app import views

urlpatterns = [
    url('^$', views.index),
    path('admin/', admin.site.urls),
    url('leaching/repair', include('leaching.repair_app.urls')),
    url('leaching', include('leaching.express_anal_app.urls')),
    url('^furnace/fractional', include('furnace.fractional_app.urls')),
    url('furnace/concentrate', include('furnace.concentrate_report_app.urls')),
    url('furnace/shihta', include('furnace.loading_shihta_app.urls')),
    url('furnace/metals', include('furnace.metals_compute_app.urls')),
    url('electrolysis/technical', include('electrolysis.technical_report_app.urls')),
    url('^auth', include('login_app.urls')),
    url('^common', include('common.all_journals_app.urls')),
]
