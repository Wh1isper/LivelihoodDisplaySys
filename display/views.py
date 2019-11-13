from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, User
from django.db.models import Count, Q

SALT = 'iloveyou'


# decorator
def auth(func):
    # written by jzs
    def inner(request, *args, **kwargs):
        try:
            # v = request.get_signed_cookie('username', salt=SALT)
            # user = User.objects.filter(user_name__exact=v)
            # if not user:
            #     return JsonResponse({"err": 2})
            if not request.session['login']:
                return JsonResponse({"err": 2})
        except:
            return JsonResponse({"err": 2})
        return func(request, *args, **kwargs)

    return inner


# decorator
def post_only(func):
    # written by jzs
    def inner(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({"err": 4})
        else:
            return func(request, *args, **kwargs)

    return inner


# decorator
def get_only(func):
    # written by jzs
    def inner(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({"err": 4})
        else:
            return func(request, *args, **kwargs)

    return inner


@csrf_exempt
@post_only
def login(request):
    # written by jzs
    code = request.POST.get('captcha', '')
    # if not code == request.session.get('check_code', None):
    #     return JsonResponse({"err": 3})  # 验证码错误

    usr = request.POST.get('username')
    pwd = request.POST.get('password')
    user = User.objects.filter(user_name__exact=usr, password__exact=pwd)
    if user:
        response = HttpResponse(json.dumps({"success": 1}), content_type="application/json")
        # response.set_signed_cookie(key='username', value=usr, salt=SALT,
        #                            secure=True,httponly=True)
        request.session['login'] = True

        # print(request.session['login'])

        return response
    else:
        return JsonResponse({"err": 2})


@csrf_exempt
@post_only
@auth
def logout(request):
    # written by jzs
    response = HttpResponse(json.dumps({"success": 1}), content_type="application/json")
    # response.delete_cookie('username')
    request.session['login'] = False
    # print(request.session['login'])
    return response


@post_only
@csrf_exempt
def register(request):
    # written by jzs
    try:
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        user = User.objects.filter(user_name__exact=usr)
        if not user:
            register_user = User(user_name=usr, password=pwd)
            register_user.save()
            return JsonResponse({"success": 1})
        else:
            return JsonResponse({"err": 101})
    except:
        return JsonResponse({"err": 1})


@csrf_exempt
@auth
@get_only
def query_count(request):
    # written by jzs
    first_category = request.GET.get('first_category')
    first_category_filter_id = request.GET.getlist('first_category_filter_id')
    second_category = request.GET.get('second_category')
    second_category_filter_id = request.GET.getlist('second_category_filter_id')
    time_after = request.GET.get('time_after')
    time_before = request.GET.get('time_before')
    ret = {}
    try:
        object_within_period = Event.objects
        # 对时间取区间
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
                    # 对第一类的每一个项按第二类统计
                    if not first_category_filter_id or value[0] in first_category_filter_id[0].split(","):
                        first_category_dict = {first_category: value}
                        cur_set = object_within_period.filter(**first_category_dict).values_list(second_category) \
                            .annotate(Count(second_category))
                        cur_dict = {}
                        all = 0
                        for x in cur_set:
                            if not second_category_filter_id or x[0] in second_category_filter_id[0].split(","):
                                # 统计所有或按id统计
                                cur_dict[x[0]] = x[1]
                                all += x[1]
                        total += all
                        ret[value] = cur_dict
                        cur_dict["all"] = all
                ret["all"] = total
                return JsonResponse(json.dumps(ret), safe=False)
            else:
                # 只统计第一类
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
    except:
        return JsonResponse(json.dumps({"err": 5}), safe=False)


@get_only
@csrf_exempt
def check_code(request):
    # written by jzs
    code = "answer is here"
    img = "img is here"

    # imagepath = path.join(d, "static/show/wordimage/" + str(news_id) + ".png")
    # print("imagepath=" + str(imagepath))
    # image_data = open(imagepath, "rb").read()

    request.session['check_code'] = code
    return HttpResponse(img, content_type="image/png")


@csrf_exempt
@auth
@get_only
def sort_info(request):
    # written by wcz
    def or_list_STREET_ID(list):
        x = Q()
        for value in list:
            x = x | Q(STREET_ID=value)
        return x

    def or_list_COMMUNITY_ID(list):
        x = Q()
        for value in list:
            x = x | Q(COMMUNITY_ID=value)
        return x

    def or_list_EVENT_TYPE_ID(list):
        x = Q()
        for value in list:
            x = x | Q(EVENT_TYPE_ID=value)
        return x

    after_leach = Event.objects.all()
    STREET_ID = request.GET.getlist('STREET')
    COMMUNITY_ID = request.GET.getlist('COMMUNITY')
    EVENT_TYPE_ID = request.GET.getlist('EVENT_TYPE')
    after_leach = Event.objects.all()

    sort = request.GET.get('sort')
    count = request.GET.get('count')
    offset = request.GET.get('offset')
    time_after = request.GET.get('time_after')
    time_before = request.GET.get('time_before')
    rec_id_before = request.GET.get('id_before')
    rec_id_after = request.GET.get('id_after')
    if time_after == None:
        time_after = '1970-01-01'
    if time_before == None:
        time_before = '2999-12-31'
    if rec_id_after == None:
        rec_id_after = -9999999
    else:
        rec_id_after = int(rec_id_after)
    if rec_id_before == None:
        rec_id_before = 9999999
    else:
        rec_id_before = int(rec_id_before)
    if sort == None:
        sort = 'id_inc'
    if count == None:
        count = 20
    else:
        count = int(count)
        if count > 100:
            return JsonResponse({"err": 5, "msg": "count too high"})
    if offset == None:
        offset = 0
    else:
        offset = int(offset)
    if STREET_ID:
        STREET_ID = STREET_ID[0].split(',')
        filter_street_id = or_list_STREET_ID(STREET_ID)
        after_leach = after_leach.filter(filter_street_id)
    if COMMUNITY_ID:
        COMMUNITY_ID = COMMUNITY_ID[0].split(',')
        filter_community_id = or_list_COMMUNITY_ID(COMMUNITY_ID)
        after_leach = after_leach.filter(filter_community_id)
    if EVENT_TYPE_ID:
        EVENT_TYPE_ID = EVENT_TYPE_ID[0].split(',')
        filter_event_type_id = or_list_EVENT_TYPE_ID(EVENT_TYPE_ID)
        after_leach = after_leach.filter(filter_event_type_id)
    if sort == 'time_inc':
        list1 = []
        inctime = after_leach.filter(CREATE_TIME__range=(time_after, time_before),
                                       REC_ID__range=(rec_id_after, rec_id_before)).order_by('CREATE_TIME')
        #if offset + count > len(inctime):
         #   return JsonResponse({"err": 5, "msg": "index out of range"})
        if offset >= len(inctime):
            return JsonResponse({"count":count,"data":[]})
        elif offset+count>len(inctime):
            inctime = inctime[offset:len(inctime)]
        else:
            inctime = inctime[offset:offset + count]
        for info in inctime:
            event_dict = {"REC_ID": info.REC_ID,
                          "REPORT_NUM": info.REPORT_NUM,
                          "CREATE_TIME": info.CREATE_TIME,
                          # "DISTRICT_NAME":info.DISTRICT_NAME,
                          "DISTRICT_ID": info.DISTRICT_ID,
                          # "STREET_NAME":info.STREET_NAME,
                          "STREET_ID": info.STREET_ID,
                          # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                          "COMMUNITY_ID": info.COMMUNITY_ID,
                          # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                          "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                          # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                          "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                          # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                          "SUB_TYPE_ID": info.SUB_TYPE_ID,
                          # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                          "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                          # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                          "EVENT_SRC_ID": info.EVENT_SRC_ID,
                          "OPERATE_NUM": info.OPERATE_NUM,
                          "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                          "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                          "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                          "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                          # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                          "OCCUR_PLACE": info.OCCUR_PLACE}
            list1.append(event_dict)
        return JsonResponse({"count": count, "data": list1})

    elif sort == 'time_dec':
        list2 = []
        dectime = after_leach.filter(CREATE_TIME__range=(time_after, time_before),
                                       REC_ID__range=(rec_id_after, rec_id_before)).order_by('-CREATE_TIME')
        if offset > len(dectime):
            return JsonResponse({"count":count,"data":[]})
        elif offset+count>len(dectime):
            dectime = dectime[offset:len(dectime)]
        else:
            dectime = dectime[offset:offset + count]
        for info in dectime:
            event_dict = {"REC_ID": info.REC_ID,
                          "REPORT_NUM": info.REPORT_NUM,
                          "CREATE_TIME": info.CREATE_TIME,
                          # "DISTRICT_NAME":info.DISTRICT_NAME,
                          "DISTRICT_ID": info.DISTRICT_ID,
                          # "STREET_NAME":info.STREET_NAME,
                          "STREET_ID": info.STREET_ID,
                          # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                          "COMMUNITY_ID": info.COMMUNITY_ID,
                          # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                          "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                          # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                          "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                          # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                          "SUB_TYPE_ID": info.SUB_TYPE_ID,
                          # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                          "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                          # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                          "EVENT_SRC_ID": info.EVENT_SRC_ID,
                          "OPERATE_NUM": info.OPERATE_NUM,
                          "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                          "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                          "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                          "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                          # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                          "OCCUR_PLACE": info.OCCUR_PLACE}
            list2.append(event_dict)
        return JsonResponse({"count": count, "data": list2})

    elif sort == 'id_inc':
        list3 = []
        incid = after_leach.extra(select={'id_inc': 'REC_ID+0'}).filter(CREATE_TIME__range=(time_after, time_before),
                                                                          REC_ID__range=(rec_id_after+1, rec_id_before-1))
        incid = incid.extra(order_by=['id_inc'])
        print(len(incid))
        if offset > len(incid):
            return JsonResponse({"count":count,"data":[]})
        elif offset+count>len(incid):
            incid = incid[offset:len(incid)]
        else:
            incid = incid[offset:offset + count]
        print(len(incid))
        # do not know what ID yet
        for info in incid:
            event_dict = {"REC_ID": info.REC_ID,
                          "REPORT_NUM": info.REPORT_NUM,
                          "CREATE_TIME": info.CREATE_TIME,
                          # "DISTRICT_NAME":info.DISTRICT_NAME,
                          "DISTRICT_ID": info.DISTRICT_ID,
                          # "STREET_NAME":info.STREET_NAME,
                          "STREET_ID": info.STREET_ID,
                          # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                          "COMMUNITY_ID": info.COMMUNITY_ID,
                          # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                          "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                          # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                          "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                          # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                          "SUB_TYPE_ID": info.SUB_TYPE_ID,
                          # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                          "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                          # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                          "EVENT_SRC_ID": info.EVENT_SRC_ID,
                          "OPERATE_NUM": info.OPERATE_NUM,
                          "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                          "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                          "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                          "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                          # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                          "OCCUR_PLACE": info.OCCUR_PLACE}
            list3.append(event_dict)
        return JsonResponse({"count": count, "data": list3})

    elif sort == 'id_dec':
        list4 = []
        decid = after_leach.extra(select={'id_dec': 'REC_ID+0'}).filter(CREATE_TIME__range=(time_after, time_before),
                                                                          REC_ID__range=(rec_id_after+1,
                                                                                         rec_id_before-1))  # do not know what ID yet
        decid = decid.extra(order_by=['-id_dec'])
        print(len(decid))
        if offset > len(decid):
            return JsonResponse({"count":count,"data":[]})
        elif offset+count>len(decid):
            decid = decid[offset:len(decid)]
        else:
            decid = decid[offset:offset + count]
        for info in decid:
            event_dict = {"REC_ID": info.REC_ID,
                          "REPORT_NUM": info.REPORT_NUM,
                          "CREATE_TIME": info.CREATE_TIME,
                          # "DISTRICT_NAME":info.DISTRICT_NAME,
                          "DISTRICT_ID": info.DISTRICT_ID,
                          # "STREET_NAME":info.STREET_NAME,
                          "STREET_ID": info.STREET_ID,
                          # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                          "COMMUNITY_ID": info.COMMUNITY_ID,
                          # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                          "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                          # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                          "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                          # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                          "SUB_TYPE_ID": info.SUB_TYPE_ID,
                          # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                          "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                          # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                          "EVENT_SRC_ID": info.EVENT_SRC_ID,
                          "OPERATE_NUM": info.OPERATE_NUM,
                          "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                          "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                          "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                          "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                          # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                          "OCCUR_PLACE": info.OCCUR_PLACE}
            list4.append(event_dict)
        return JsonResponse({"count": count, "data": list4})
    else:
        return JsonResponse({"err": 1})



@csrf_exempt
@auth
@get_only
def item(request):
    # written by jzs
    rec_id = request.GET.get('REC_ID')
    if rec_id:
        try:
            info = Event.objects.get(REC_ID__exact=rec_id)
            event_dict = {"REC_ID": info.REC_ID,
                          "REPORT_NUM": info.REPORT_NUM,
                          "CREATE_TIME": info.CREATE_TIME,
                          # "DISTRICT_NAME":info.DISTRICT_NAME,
                          "DISTRICT_ID": info.DISTRICT_ID,
                          # "STREET_NAME":info.STREET_NAME,
                          "STREET_ID": info.STREET_ID,
                          # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                          "COMMUNITY_ID": info.COMMUNITY_ID,
                          # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                          "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                          # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                          "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                          # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                          "SUB_TYPE_ID": info.SUB_TYPE_ID,
                          # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                          "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                          # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                          "EVENT_SRC_ID": info.EVENT_SRC_ID,
                          "OPERATE_NUM": info.OPERATE_NUM,
                          "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                          "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                          "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                          "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                          # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                          "OCCUR_PLACE": info.OCCUR_PLACE}
            return JsonResponse(event_dict)
        except:
            return JsonResponse({"err": 5})
    else:
        return JsonResponse({"err": 5})


@csrf_exempt
@auth
@get_only
def warning(request):
    # written by jzs
    time_after = request.GET.get('time_after')
    time_before = request.GET.get('time_before')
    begin = request.GET.get('begin', 0)
    count = request.GET.get('count', 20)
    warning_event = Event.objects.filter(Q(EVENT_TYPE_ID__exact='1') | Q(MAIN_TYPE_ID__exact='93')|
                                         Q(SUB_TYPE_ID__exact='832')| Q(SUB_TYPE_ID__exact='833')).order_by('-CREATE_TIME')

    try:
        object_within_period = warning_event
        if time_after:
            object_within_period = object_within_period.filter(CREATE_TIME__gte=time_after)
        if time_before:
            object_within_period = object_within_period.filter(CREATE_TIME__lte=time_before)
        object_in_scale = object_within_period[begin:begin + count]
    except:
        return JsonResponse({"err": 5})
    count = 0
    ret_list = []
    for info in object_in_scale:
        count += 1
        event_dict = {"REC_ID": info.REC_ID,
                      "REPORT_NUM": info.REPORT_NUM,
                      "CREATE_TIME": info.CREATE_TIME,
                      # "DISTRICT_NAME":info.DISTRICT_NAME,
                      "DISTRICT_ID": info.DISTRICT_ID,
                      # "STREET_NAME":info.STREET_NAME,
                      "STREET_ID": info.STREET_ID,
                      # "COMMUNITY_NAME":info.COMMUNITY_NAME,
                      "COMMUNITY_ID": info.COMMUNITY_ID,
                      # "EVENT_TYPE_NAME":info.VENT_TYPE_NAME,
                      "EVENT_TYPE_ID": info.EVENT_TYPE_ID,
                      # "MAIN_TYPE_NAME":info.MAIN_TYPE_NAME,
                      "MAIN_TYPE_ID": info.MAIN_TYPE_ID,
                      # "SUB_TYPE_NAME":info.SUB_TYPE_NAME,
                      "SUB_TYPE_ID": info.SUB_TYPE_ID,
                      # "DISPOSE_UNIT_NAME":info.DISPOSE_UNIT_NAME,
                      "DISPOSE_UNIT_ID": info.DISPOSE_UNIT_ID,
                      # "EVENT_SRC_NAME":info.EVENT_SRC_NAME,
                      "EVENT_SRC_ID": info.EVENT_SRC_ID,
                      "OPERATE_NUM": info.OPERATE_NUM,
                      "OVERTIME_ARCHIVE_NUM": info.OVERTIME_ARCHIVE_NUM,
                      "INTIME_TO_ARCHIVE_NUM": info.INTIME_TO_ARCHIVE_NUM,
                      "INTIME_ARCHIVE_NUM": info.INTIME_ARCHIVE_NUM,
                      "EVENT_PROPERTY_ID": info.EVENT_PROPERTY_ID,
                      # "EVENT_PROPERTY_NAME":info.EVENT_PROPERTY_NAME,
                      "OCCUR_PLACE": info.OCCUR_PLACE}
        ret_list.append(event_dict)
    return JsonResponse({"count": count, "data": ret_list})


# @auth
def init(request):
    with open('display/static/display/data/data.json', 'r', encoding='utf-8') as f:
        content = f.read()
    result = json.loads(content[1:-1])
    for line in result:
        event = Event(
            REC_ID=eval(line['REC_ID']),
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

def to_main_page(request):
    return HttpResponseRedirect("https://test.nzh21.site/")