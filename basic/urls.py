from django.urls import path

from . import views

urlpatterns = [
    path('', views.logfile, name='logfile'),
    path('log', views.testlog, name='testlog'),
    path('chkrun', views.bool_running, name='chkrun')
]