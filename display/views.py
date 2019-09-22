from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, User
from django.db.models import Count


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
def post_only(func):
    def inner(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({"err": "3"})
        else:
            return func(request, *args, **kwargs)

    return inner


# decorator
def get_only(func):
    def inner(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({"err": "3"})
        else:
            return func(request, *args, **kwargs)

    return inner


@csrf_exempt
@post_only
def login(request):
    usr = request.POST.get('username')
    pwd = request.POST.get('password')
    user = User.objects.filter(user_name__exact=usr, password__exact=pwd)
    if user:
        response = HttpResponse(json.dumps({"success": "0"}), content_type="application/json")
        response.set_signed_cookie(key='username', value=usr, salt='iloveyou')
        return response
    else:
        return JsonResponse({"err": "1"})


@csrf_exempt
@post_only
@auth
def logout(request):
    response = HttpResponse(json.dumps({"success": "0"}), content_type="application/json")
    response.delete_cookie('username')
    return response


@post_only
@csrf_exempt
def register(request):
    try:
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        user = User.objects.filter(user_name__exact=usr)
        if not user:
            register_user = User(user_name=usr, password=pwd)
            register_user.save()
            return JsonResponse({"success": "0"})
        else:
            return JsonResponse({"err": "2"})
    except:
        return JsonResponse({"err": "0"})


@csrf_exempt
@auth
@get_only
def query_count(request):
    first_category = request.GET.get('first_category')
    first_category_filter_id = request.GET.getlist('first_category_filter_id')
    second_category = request.GET.get('second_category')
    second_category_filter_id = request.GET.getlist('second_category_filter_id')
    time_after = request.GET.get('time_after')
    time_before = request.GET.get('time_before')
    ret = {}
    if True:
    # try:
        object_within_period = Event.objects
        if time_after:
            object_within_period = object_within_period.filter(CREATE_TIME__gte=time_after)
        if time_before:
            object_within_period = object_within_period.filter(CREATE_TIME__lte=time_before)
        if first_category:
            if second_category:
                first_category_set = object_within_period.values_list(first_category).distinct()
                first_category_set_list = [x[0] for x in first_category_set]
                total = 0
                for value in first_category_set_list:
                    if not first_category_filter_id or value[0] in first_category_filter_id[0].split(","):
                        first_category_dict = {first_category: value}
                        cur_set = object_within_period.filter(**first_category_dict).values_list(second_category) \
                            .annotate(Count(second_category))
                        cur_dict = {}
                        all = 0
                        for x in cur_set:
                            if not second_category_filter_id or x[0] in second_category_filter_id[0].split(","):
                                cur_dict[x[0]] = x[1]
                                all += x[1]
                        total += all
                        ret[value] = cur_dict
                        cur_dict["all"] = all
                ret["all"] = total
                return JsonResponse(json.dumps(ret), safe=False)
            else:
                first_category_set = object_within_period.values_list(first_category).annotate(Count(first_category))
                total = 0
                for x in first_category_set:
                    if not first_category_filter_id or x[0] in first_category_filter_id[0].split(","):
                        ret[x[0]] = x[1]
                        total += x[1]
                ret["all"] = total
                return JsonResponse(json.dumps(ret), safe=False)
        else:
            return JsonResponse(json.dumps({"all": len(object_within_period.all())}), safe=False)
    # except:
    #     return JsonResponse(json.dumps({"err": 4}), safe=False)


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


