from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os
import psutil
import sys
from subprocess import Popen
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse


def geeks_view(request):
    # render function takes argument  - request
    # and return HTML as response
    return render(request, "templates/index.html")


def testlog(request):
    file_map = {
        "dm_report_gen.py": "dm_log",
        "db_refresh.py": "refresh_log",
        "start_bot.py": "auto_insta.log"}

    f_name = file_map.get(request.GET.get('file_name'))
    f_path = os.path.join("..", "auto-insta", f_name)

    # orignal path, DO NO DELETE
    # file_ = open(os.path.join("..", "auto-insta", "auto_insta.log"))
    # file_ = open(os.path.abspath(f_path))
    file_ = open(f_path)
    # return HttpResponse(file_)
    return JsonResponse({'data': file_.readlines()})


def bool_running(request):
    process_name = request.GET.get('file_name')
    flag = False
    for process in psutil.process_iter():
        # check if python process & then check if process name == filename
        if process.name() == 'python' and process_name in process.cmdline()[1]:
            print(process)
            print(process.cmdline())
            flag = True
            break
    return JsonResponse({'status': flag})
