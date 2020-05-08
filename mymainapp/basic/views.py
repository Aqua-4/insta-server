from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings



def logfile(request):

    return HttpResponse("Hello Welcome")    

def testlog(request):
    file_ = open(os.path.join(settings.BASE_DIR, 'test.log'))
    return HttpResponse(file_)    
