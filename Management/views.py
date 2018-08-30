from django.http import HttpResponse
from Management.models import Volunteer
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import json


def volunteer_query(request):
    stu_id = request.GET.get("stu_id")
    password = request.GET.get("password")
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        msg = {
            "result": "No Student Found !",
            "stu_id": stu_id,
        }
        return HttpResponse(
            json.dumps(msg)
        )
    if password == stu.password:
        msg = {
            "result": 1,
            "name": stu.name_zh,
            "stu_id": stu.stu_id,
            "volunteer_time": stu.time_volunteer
        }
        return HttpResponse(
            json.dumps(msg)
        )
    else:
        msg = {
            "result": "Wrong Password !",
            "stu_id": stu_id
        }
        return HttpResponse(
            json.dumps(msg)
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


@login_required()
def volunteer_input(request):
    stu_id = request.GET.get("stu_id")
    time = request.GET.get("time")
    try:
        stu = Volunteer.objects.get(stu_id=stu_id)
    except:
        return HttpResponse("Wrong Student !")
    time_old = stu.time_volunteer
    time_new = time_old + time
    stu.time_volunteer = time_new
    stu.save()
    msg = {
        "result": 1,
        "stu_id": stu_id,
        "time": stu.time_volunteer
    }
    return HttpResponse(
        json.dumps(msg)
    )


def manager_import(request):
    pass
