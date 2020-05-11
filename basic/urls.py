from django.urls import path

from . import views

urlpatterns = [
    path('log', views.testlog, name='testlog'),
    path('chkrun', views.bool_running, name='chkrun'),
    path('', views.geeks_view, name='index')
]
