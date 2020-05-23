from django.urls import path

from . import views

urlpatterns = [
    path('log', views.testlog, name='testlog'),
    path('get_visual', views.get_visual, name='get_visual'),
    path('chkrun', views.bool_running, name='chkrun'),
    path('', views.geeks_view, name='index')
]
