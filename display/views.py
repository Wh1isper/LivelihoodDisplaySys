from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, User


# decorator
def auth(func):
    def inner(request, *args, **kwargs):
        try:
            v = request.get_signed_cookie('username', salt='iloveyou')
            user = User.objects.filter(user_name__exact=v)
            if not user:
                return JsonResponse({"err": "1"})
        except:
            return JsonResponse({"err": "1"})
        return func(request, *args, **kwargs)

    return inner


# decorator
def post_only_methon(func):
    def inner(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({"err": "3"})
        else:
            return func(request, *args, **kwargs)
    return inner

@post_only_methon
@csrf_exempt
def login(request):
    usr = request.POST.get('username')
    pwd = request.POST.get('password')
    user = User.objects.filter(user_name__exact=usr, password__exact=pwd)
    if user:
        response = HttpResponse(json.dumps({"msg": "login"}), content_type="application/json")
        response.set_signed_cookie(key='username', value=usr, salt='iloveyou')
        return response
    else:
        return JsonResponse({"err": "1"})


@post_only_methon
@csrf_exempt
@auth
def logout(request):
    response = HttpResponse(json.dumps({"msg": "logout"}), content_type="application/json")
    response.delete_cookie('username')
    return response


@post_only_methon
@csrf_exempt
def register(request):
    try:
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        user = User.objects.filter(user_name__exact=usr)
        if not user:
            register_user = User(user_name=usr, password=pwd)
            register_user.save()
            return JsonResponse({"msg": "register"})
        else:
            return JsonResponse({"err": "2"})
    except:
        return JsonResponse({"err": "0"})


def init(request):
    with open('display/static/display/data/data.json', 'r', encoding='utf-8') as f:
        content = f.read()
    result = json.loads(content[1:-1])
    for line in result:
        event = Event(
            REC_ID=line['REC_ID'],
            REPORT_NUM=line['REPORT_NUM'],
            CREATE_TIME=line['CREATE_TIME'],
            DISTRICT_NAME=line['DISTRICT_NAME'],
            DISTRICT_ID=line['DISTRICT_ID'],
            STREET_NAME=line['STREET_NAME'],
            STREET_ID=line['STREET_ID'],
            COMMUNITY_NAME=line['COMMUNITY_NAME'],
            COMMUNITY_ID=line['COMMUNITY_ID'],
            EVENT_TYPE_NAME=line['EVENT_TYPE_NAME'],
            EVENT_TYPE_ID=line['EVENT_TYPE_ID'],
            MAIN_TYPE_NAME=line['MAIN_TYPE_NAME'],
            MAIN_TYPE_ID=line['MAIN_TYPE_ID'],
            SUB_TYPE_NAME=line['SUB_TYPE_NAME'],
            SUB_TYPE_ID=line['SUB_TYPE_ID'],
            DISPOSE_UNIT_NAME=line['DISPOSE_UNIT_NAME'],
            DISPOSE_UNIT_ID=line['DISPOSE_UNIT_ID'],
            EVENT_SRC_NAME=line['EVENT_SRC_NAME'],
            EVENT_SRC_ID=line['EVENT_SRC_ID'],
            OPERATE_NUM=line['OPERATE_NUM'],
            OVERTIME_ARCHIVE_NUM=line['OVERTIME_ARCHIVE_NUM'],
            INTIME_TO_ARCHIVE_NUM=line['INTIME_TO_ARCHIVE_NUM'],
            INTIME_ARCHIVE_NUM=line['INTIME_ARCHIVE_NUM'],
            EVENT_PROPERTY_ID=line['EVENT_PROPERTY_ID'],
            EVENT_PROPERTY_NAME=line['EVENT_PROPERTY_NAME'],
            OCCUR_PLACE=line['OCCUR_PLACE'],
        )
        event.save()
    return HttpResponse("添加完成")
