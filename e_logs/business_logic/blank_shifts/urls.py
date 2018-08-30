from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('test2/', set_limited_access_employee_list),

]
