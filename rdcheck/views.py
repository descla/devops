from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from datetime import datetime, date
import pdb


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


def test(request):
    context = {'latest_question_list': [{'id': 1, 'question_text': 'abc'}, {'id': 2, 'question_text': 'cc'}, ]}
    return render(request, 'rdcheck/test.html', context)



def linux_roundcheck(request):
    pass
