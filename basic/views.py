from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os
import psutil
import sys
from subprocess import Popen


def logfile(request):

    return HttpResponse("Hello Welcome")


def testlog(request):

    # orignal path, DO NO DELETE
    # file_ = open(os.path.join("..", "auto-insta", "auto_insta.log"))
    file_ = open(os.path.join("auto_insta.log"))
    return HttpResponse(file_)


def bool_running(request):

    # need json response
    process_name = "tmp.py"

    flag = False
    for process in psutil.process_iter():
        # check if python process & then check if process name == filename
        if process.name() == 'python' and process_name in process.cmdline()[1]:
            print(process)
            print(process.cmdline())
            flag = True
            break
    return HttpResponse(flag)
