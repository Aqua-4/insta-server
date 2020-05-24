from django.urls import path

from . import views

urlpatterns = [
    path('log', views.testlog, name='testlog'),
    path('get_visual', views.get_visual, name='get_visual'),
    path('get_smart_log', views.get_smart_log, name='get_smart_log'),
    path('get_calendar_dates', views.get_calendar_dates, name='get_calendar_dates'),
    path('chkrun', views.bool_running, name='chkrun'),
    path('', views.geeks_view, name='index')
]
