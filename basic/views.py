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

    # orignal path, DO NO DELETE
    # file_ = open(os.path.join("..", "auto-insta", "auto_insta.log"))
    file_ = open(os.path.join("auto_insta.log"))
    return HttpResponse(file_)


def bool_running(request):
    process_name = request.GET.get('file_name', "tmp.py")
    flag = False
    for process in psutil.process_iter():
        # check if python process & then check if process name == filename
        if process.name() == 'python' and process_name in process.cmdline()[1]:
            print(process)
            print(process.cmdline())
            flag = True
            break
    return JsonResponse({'status': flag})
