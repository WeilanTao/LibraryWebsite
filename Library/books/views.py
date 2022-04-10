from django.shortcuts import render
from django.http import HttpResponse

import sys 
import os

# Create your views here.
def index(request):

    return HttpResponse("this is: ", sys.path.append(os.path.dirname(os.path.abspath('.'))))


