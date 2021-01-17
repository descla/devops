from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime, date, timedelta
import pdb
from .models import t_linux_result
from inventory.models import t_hosts


# Create your views here.

class JsonCustomEncoder(json.JSONEncoder):
    """
    自定义一个支持序列化时间格式的类
    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)


def index(request):
    return HttpResponse("Hello,world.You are at the roundcheck index")


def linux_roundcheck(request):
    if request.method == 'GET':
        today = datetime.now()
        p1 = timedelta(days=1)
        hosts = t_linux_result.objects.filter(ts__range=[today.date(), (today+p1).date()])
    return render(request, 'rdcheck/os_linux.html', hosts)

def oracle_roundcheck(request):
    pass
