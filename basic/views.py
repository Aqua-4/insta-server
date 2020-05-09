from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings


def logfile(request):

    return HttpResponse("Hello Welcome")


def testlog(request):

    # orignal path, DO NO DELETE
    # file_ = open(os.path.join("..", "auto-insta", "auto_insta.log"))
    file_ = open(os.path.join("auto_insta.log"))
    return HttpResponse(file_)


def bool_running(request):
    # need json response
    import psutil
    import sys
    from subprocess import Popen

    for process in psutil.process_iter():
        if process.cmdline() == ['python', 'your_script.py']:
            return True
        else:
            return False
