from django.http import HttpResponse
from Management.models import Volunteer, Activity, MyActivity
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import json


def query_base(stu_id, name_zh, phone_num):
    msg = dict()
    myactivity_dict = dict()
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        msg = {
            "msg": "No Student Found !"
        }
        return msg
    if (stu.name_zh == name_zh) and (stu.phone_num == phone_num):
        activity_list = stu.myactivity_set.all()
        for i in activity_list:
            myactivity_dict[i.activity.title
                            + '.' + str(i)[-2:-1] ] = i.mytime
        time = stu.time_volunteer
        msg = {
            "time": time,
            "activities": myactivity_dict
        }
        return msg
    else:
        msg = {
            "msg": "Wrong Information !"
        }
        return msg


def volunteer_query(request):
    stu_id = request.GET.get("stu_id")
    name_zh = request.GET.get("name")
    phone_num = request.GET.get("phone")
    msg = query_base(stu_id=stu_id, name_zh=name_zh, phone_num=phone_num)
    return HttpResponse(
        json.dumps(msg)
    )


def register_base(stu_id, password, name_zh, phone_num):
    try:
        stu = Volunteer.objects.create(stu_id=stu_id, name_zh=name_zh,
                                       password=password, phone_num=phone_num)
        msg = {
            "result": 1
        }
        stu.time_volunteer = 0
    except:
        msg = {
            "result": "Create Error !"
        }
    return msg


def volunteer_register(request):
    stu_id = request.GET.get("stu_id")
    password = request.GET.get("password")
    name_zh = request.GET.get("name")
    phone_num = request.GET.get("phone")
    msg = register_base(stu_id=stu_id, password=password,
                  name_zh=name_zh, phone_num=phone_num)
    return msg


def manager_login(request):
    user = request.GET.get("username")
    pwd = request.GET.get("pwd")
    manager = authenticate(username=user, password=pwd)
    if manager:
        auth.login(request, manager)
        msg = {
            "result": 1
        }
        return HttpResponse(
            json.dumps(msg)
        )
    else:
        msg = {
            "result": "Login Error !"
        }
        return HttpResponse(
            json.dumps(msg)
        )


def manager_logout(request):
    pass


# @login_required()
def activity_add_base(title, group):
    try:
        activity = Activity.objects.create(title=title, group=group)
        msg = {
            "result": 1
        }
    except:
        msg =  {
            "msg": "error in creating activity"
        }
    return msg


def manager_add_activity(request):
    title = request.GET.get("title")
    group = request.GET.get("group")
    msg = activity_add_base(title, group)
    return HttpResponse(
        json.dumps(msg)
    )


def import_base(stu_id, activity_title, time):
    mypartin = MyActivity()
    mypartin.mytime = time
    try:
        activity = Activity.objects.get(title=activity_title)
    except:
         msg = {
             "msg": "no act found !"
         }
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
         msg = {
             "msg": "nobody found !"
         }

    mypartin.person = stu
    mypartin.activity = activity
    mypartin.save()
    mylist = stu.myactivity_set.all()
    myalltime = 0
    for i in mylist:
        myalltime += i.mytime
    stu.time_volunteer = myalltime
    stu.save()
    msg = {
        "result": 1
    }
    return msg


def single_import(request):
    stu_id = request.GET.get("stu_id")
    activity_title = request.GET.get("activity_title")
    time = request.GET.get("time")
    msg = import_base(stu_id, activity_title, time)
    print(msg)
    return HttpResponse(
        json.dumps(msg)
    )


def manager_import(request):
    pass

