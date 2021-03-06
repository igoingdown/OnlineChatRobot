# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime
from test_python_call_shell import foo
from qiniu import *
from qiniu_util import upload_to_cloud
from save_my_doc import save_md_files_into_database

# Create your views here.

def show_blogs(request):
    tag_lists = Post.objects.all()
    return render(request, 'blogApp/index1.html',
                  context={'post_list': tag_lists})


def submit(request):
    return render(request, 'blogApp/form.html',
                  context={'welcome': '欢迎'})
    pass


def show_ajax_test_form(request):
    return render(request, 'blogApp/ajax_test.html')


def comments_upload(request):
    if request.method == 'POST':
        print "it's a test"
        print request.POST['name']
        print request.POST['password']

        return HttpResponse("表单测试成功")
    else:
        return HttpResponse("<h1>test</h1>")



@csrf_exempt
def investigate(request):
    if request.method == 'POST':
        print 'Raw Data: "%s"' % request.body
        params = {'key': '34a937c951c84cb3aaa855e54fda653e',
                  'info': '你好'}
        forward = HistoryMessage(create_time=datetime.datetime.now(),
                                 modified_time=datetime.datetime.now(),
                                 body="你好", talk_direction=0)
        forward.save()
        r = requests.post("http://www.tuling123.com/openapi/api", data=params)
        if r.status_code == 200:
            data = json.loads(r.text)
            data['time'] = datetime.datetime.now()
            with open("./blogApp/demo/bin/source.txt", "w") as f:
                f.write(data['text'])
            backward = HistoryMessage(create_time=datetime.datetime.now(),
                                     modified_time=datetime.datetime.now(),
                                     body=params['info'], talk_direction=1,
                                     type=data['code'])
            backward.save()
    return JsonResponse(data)


@csrf_exempt
def stores(request):
    if request.method == 'POST':
        print 'Raw Data: "%s"' % request.body
        params = {'key': '34a937c951c84cb3aaa855e54fda653e',
                  'info': '北京到哈尔滨的火车'}
        forward = HistoryMessage(create_time=datetime.datetime.now(),
                                 modified_time=datetime.datetime.now(),
                                 talk_direction=0,
                                 body="北京到哈尔滨的火车")
        forward.save()
        r = requests.post("http://www.tuling123.com/openapi/api", data=params)
        if r.status_code == 200:
            d = json.loads(r.text)
            d['time'] = datetime.datetime.now()
            backward = HistoryMessage(create_time=datetime.datetime.now(),
                                      modified_time=datetime.datetime.now(),
                                      talk_direction=1,
                                      body=params['info'],
                                      url_body=d['url'],
                                      type=d['code'])
            backward.save()
            with open("./blogApp/demo/bin/source.txt", "w") as f:
                f.write(d['text'])
    return JsonResponse(d)


@csrf_exempt
def flight(request):
    if request.method == 'POST':
        print 'Raw Data: "%s"' % request.body
        params = {'key': '34a937c951c84cb3aaa855e54fda653e',
                  'info': '明天北京到拉萨的飞机'}
        forward = HistoryMessage(create_time=datetime.datetime.now(),
                                 modified_time=datetime.datetime.now(),
                                 talk_direction=0,
                                 body=params['info'])
        forward.save()
        r = requests.post("http://www.tuling123.com/openapi/api", data=params)
        if r.status_code == 200:
            d = json.loads(r.text)
            d['time'] = datetime.datetime.now()
            print d['text']
            with open('./blogApp/demo/bin/source.txt', 'w') as f:
                f.write("am")
            backward = HistoryMessage(create_time=datetime.datetime.now(),
                                      modified_time=datetime.datetime.now(),
                                      talk_direction=1,
                                      body='明天北京到拉萨的飞机',
                                      url_body=d['url'],
                                      type=d['code'])
            backward.save()
    return JsonResponse(d)



