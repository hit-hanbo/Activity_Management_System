from django.http import HttpResponse
from Management.models import Volunteer, Activity, MyActivity
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import json


def volunteer_query(request):
    stu_id = request.GET.get("stu_id")
    name_zh = request.GET.get("name_zh")
    phone_num = request.GET.get("phonenum")
    myactivity_dict = dict()
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        return HttpResponse(
            json.dumps({"msg": "No Student Found !"})
        )
    if (stu.name_zh == name_zh) and (stu.phone_num == phone_num):
        activity_list = stu.myactivity_set.all()
        for i in activity_list:
            myactivity_dict[i.activity.title] = i.mytime
        time = stu.time_volunteer
        return HttpResponse(
            json.dumps({
                "time": time,
                "activities": str(myactivity_dict)
            })
        )
    else:
        return HttpResponse(
            json.dumps({"msg": "Wrong Information !"})
        )


def volunteer_register(request):
    stu_id = request.GET.get("stu_id")
    password = request.GET.get("password")
    name_zh = request.GET.get("name_zh")
    phone_num = request.GET.get("phone_num")
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
            "result": "Login Error !"
        }
        return HttpResponse(
            json.dumps(msg)
        )


def manager_logout(request):
    pass


# @login_required()
def volunteer_input(request):
    stu_id = request.GET.get("stu_id")
    activity_title = request.GET.get("activity_title")
    time = request.GET.get("time")
    mypartin = MyActivity()
    mypartin.mytime = time
    try:
        activity = Activity.objects.get(title=activity_title)
    except:
        return HttpResponse(json.dumps({"msg": "no act found !"}))
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        return HttpResponse(json.dumps({"msg": "nobody found !"}))

    mypartin.person = stu
    mypartin.activity = activity
    mypartin.save()
    mylist = stu.myactivity_set.all()
    myalltime = 0
    for i in mylist:
        myalltime += i.mytime
    stu.time_volunteer = myalltime
    stu.save()
    return HttpResponse("OK !")


def manager_import(request):
    pass
