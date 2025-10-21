import json

from django.http import HttpResponse
from django.shortcuts import render
from utils.modbusTcpUtils import ModbusTcpUtils
import modbus_tk.defines as cst
from models.models import *
from django.utils import timezone


# Create your views here.
def to_sub02(request):
    return render(request, "task2.html")


# TODO 在适当位置声明变量alarm_body与alarm_smoke，分别用于记录人感报警状态和烟感报警状态
alarm_body = False
alarm_smoke = False


def get_data(request):
    conn = ModbusTcpUtils.get_conn2()
    global alarm_body, alarm_smoke
    # TODO 获取烟感探测器和人感探测器数据
    data = conn.execute(1, cst.READ_DISCRETE_INPUTS, 4, 2)

    # TODO 根据烟感和人感报警状态，控制报警灯状态
    conn.execute(1, cst.WRITE_MULTIPLE_COILS, 0, 3, [data[1], 0, data[0]])
    # TODO 根据烟感报警状态，控制门锁状态，判断当报警为连续报警时不保存数据库,否则将报警信息保存至数据库
    if data[1] == 1:
        conn.execute(1, cst.WRITE_SINGLE_COIL, 3, 1, 0)
        if not alarm_smoke:
            sen_data = SensingData(
                type=1,
                create_time=timezone.now()
            )
            sen_data.save()
    # TODO 根据人感报警状态，判断当报警为连续报警时不保存数据库,否则将报警信息保存至数据库
    if data[0] == 1:
        if not alarm_body:
            sen_data = SensingData(
                type=2,
                create_time=timezone.now()
            )
            sen_data.save()
    # TODO 记录报警状态
    alarm_body = data[0] == 1
    alarm_smoke = data[1] == 1

    return HttpResponse(json.dumps(data))


def set_data(request):
    conn = ModbusTcpUtils.get_conn2()
    global alarm_smoke
    # TODO 判断当前报警状态，当状态为无报警时，将电磁门锁置为锁定状态
    if not alarm_smoke:
        conn.execute(1, cst.WRITE_SINGLE_COIL, 3, 1, 1)
    return HttpResponse(json.dumps({}))
