# -*- coding : utf-8 -*-

from django.http import HttpResponse
from Management.models import Volunteer, Activity, MyActivity
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import json


def query_base(stu_id, name_zh):
    msg = dict()
    myactivity_dict = dict()
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        msg = {
            "result": 0,
            "msg": "No Student Found !"
        }
    if stu.name_zh == name_zh:
        activity_list = stu.myactivity_set.all()
        for i in activity_list:
            myactivity_dict[i.activity.title
                            + '.' + str(i)[-2:-1]] = i.mytime
        time = stu.time_volunteer
        msg = {
            "result": 1,
            "time": time,
            "name_zh": stu.name_zh,
            "activities": myactivity_dict
        }
    else:
        msg = {
            "result": 0,
            "msg": "Wrong Information !"
        }
    return msg


def volunteer_query(request):
    stu_id = request.GET.get("stu_id")
    name_zh = request.GET.get("name_zh")
    msg = query_base(stu_id=stu_id, name_zh=name_zh)
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
            "result": 1,
            "msg": "Create Error !"
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
            "result": 0,
            "msg": "Login Error !"
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
        msg = {
            "result": 0,
            "msg": "Error in Creating Activity"
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
    try:
        activity = Activity.objects.get(title=activity_title)
    except:
         msg = {
             "result": 0,
             "msg": "No Act Found !"
         }
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        stu = None
        msg = {
             "result": 0,
             "msg": "nobody found !"
         }
    if stu.myactivity_set.all():
        if stu.myactivity_set.get(activity__title=activity_title):
            msg = {
                "result": 0,
                "msg": "Record Exist !"
         }
    else:
        mypartin = MyActivity()
        mypartin.mytime = time
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

