from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime, date
import pdb


def index(request):
    return HttpResponse("Hello,world.You are at the inventory index")


def hosts(request):
    pass
