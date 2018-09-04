# -*- coding : utf-8 -*-

from django.http import HttpResponse
from Management.models import Volunteer, Activity, MyActivity
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import json
import os
from SheetHandler.SheetHandler import SheetHandler


def query_base(stu_id, name_zh):
    msg = dict()
    myactivity_dict = dict()
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except Volunteer.DoesNotExist:
        msg = {
            "result": 0,
            "msg": "No Student Found !"
        }
    if name_zh == stu.name_zh:
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
                                       password=password, phone_num=phone_num,
                                       time_volunteer=0)
        stu.save()
        return {"msg": "Success", "stu": stu}
    except:
        return {"msg": "Duplicate"}


def volunteer_register(request):
    stu_id = request.GET.get("stu_id")
    password = request.GET.get("password")
    name_zh = request.GET.get("name_zh")
    phone_num = request.GET.get("phone_num")
    msg = register_base(stu_id=stu_id, password=password,
                        name_zh=name_zh, phone_num=phone_num)
    msg["stu"] = ""
    return HttpResponse(
        json.dumps(msg)
    )


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


def import_base(stu_id, activity_title, time, name_zh):
    new_time = 0
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except Volunteer.DoesNotExist:
        stu = register_base(stu_id=stu_id, password="123456",
                            name_zh=name_zh, phone_num="0")["stu"]
        print("REGISTER !")
    act = Activity.objects.get(title=activity_title)
    print(stu)
    if stu:
        if name_zh == stu.name_zh:
            myact = MyActivity.objects.create(activity=act, person=stu, mytime=time)
            myact.save()
            myall_act = stu.myactivity_set.all()
            for act in myall_act:
                new_time += act.mytime
            stu.time_volunteer = new_time
            stu.save()
            return 1
        return 0


def single_import(request):
    stu_id = request.GET.get("stu_id")
    activity_title = request.GET.get("activity_title")
    time = request.GET.get("time")
    name_zh = request.GET.get("name_zh")
    msg = import_base(stu_id, activity_title, time, name_zh)
    print(msg)
    return HttpResponse(
        json.dumps(msg)
    )


def manager_import(request):
    pass


def manager_excel_import(request):
    msg = dict()
    workbook = request.FILES["Excel"]
    activity_title = request.POST.get("activity_title")
    file_name = ".\\excel\\" + str(activity_title) + ".xlsx"

    with open(file_name, "wb+") as destination:
        for chunk in workbook.chunks():
            destination.write(chunk)
    sheet = SheetHandler(file_name=file_name)
    if not sheet:
        msg = {
            "result": 0,
            "msg": "Error !"
        }
    else:
        i = 0
        sheet.resolve_sheet()
        act_list = sheet.generate_info()
        for act in act_list:
            i += 1
            import_base(act["stu_id"], activity_title,
                        act["time"], act["name_zh"])
            msg[str(i)] = {
                "stu_id": act["stu_id"],
                "time": act["time"]
            }
        print(msg)
    return HttpResponse(
        json.dumps(msg)
    )
