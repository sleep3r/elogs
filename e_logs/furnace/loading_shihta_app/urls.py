from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.furnace.loading_shihta_app import views
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url('loading$', views.index),
    url('^$', views.index)
]