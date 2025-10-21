import json

from django.db.models import Avg, Count, Case, When, IntegerField
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render

from models.models import *


# Create your views here.

def to_sub04(request):
    return render(request, "task4.html")


def get_line_data(request):
    # TODO 从数据库查询出近10分钟内，每分钟的平均温度、最大温度、平均湿度、最大湿度与记录时间等环境数据
    line_data = EnvData.objects.order_by('-create_time').extra(
        select={'create_time': 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i")'}).values(
        "create_time").annotate(avg_temp=Avg('temp'), max_temp=Max('temp'), avg_humi=Avg('humi'), max_humi=Max('humi'))[:10]

    x_list = []
    y_avg_temp = []
    y_max_temp = []
    y_avg_humi = []
    y_max_humi = []

    # TODO 封装图表所需数据，将记录时间、平均温度、最大温度、平均湿度、最大湿度分别封装到x_list、y_avg_temp、y_max_temp、y_avg_humi、y_max_humi中
    for data in line_data:
        x_list.append(data['create_time'])
        y_avg_temp.append(data['avg_temp'])
        y_max_temp.append(data['max_temp'])
        y_avg_humi.append(data['avg_humi'])
        y_max_humi.append(data['max_humi'])

    return HttpResponse(json.dumps(
        {"x_list": x_list,
         "y_avg_temp": y_avg_temp,
         "y_max_temp": y_max_temp,
         "y_avg_humi": y_avg_humi,
         "y_max_humi": y_max_humi}))


def get_bar_data(request):
    # TODO 从数据库查询出近10分钟内，每分钟的内的人感报警数量、烟感报警数量与记录时间等环境数据
    bar_data = SensingData.objects.order_by('-create_time').extra(
        select={'create_time': 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i")'}).values(
        "create_time").annotate(body_count=Count(Case(When(type=1, then=1), output_field=IntegerField())),
                                smoke_count=Count(Case(When(type=2, then=1), output_field=IntegerField())))[:10]

    x_list = []
    y_smoke_count = []
    y_body_count = []

    # TODO 封装图标所需数据，将记录时间、平均温度、最大温度、平均湿度、最大湿度分别封装到x_list、y_avg_temp、y_max_temp、y_avg_humi、y_max_humi中
    for data in bar_data:
        x_list.append(data['create_time'])
        y_smoke_count.append(data['smoke_count'])
        y_body_count.append(data['body_count'])

    return HttpResponse(json.dumps(
        {"x_list": x_list,
         "y_smoke_count": y_smoke_count,
         "y_body_count": y_body_count}))