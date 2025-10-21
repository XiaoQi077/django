import json

from django.http import HttpResponse
from django.shortcuts import render

from utils.modbusTcpUtils import ModbusTcpUtils
import modbus_tk.defines as cst

from models.models import *
from django.utils import timezone


# Create your views here.

def to_sub01(request):
    return render(request, "task1.html")


def get_data(request):
    conn = ModbusTcpUtils.get_conn1()
    # TODO 读取十合一传感器数据并转换为list类型，并根据任务书中的换算规则进行换算
    data = conn.execute(1, cst.READ_HOLDING_REGISTERS, 0, 11)
    data = list(data)
    data[4] = data[4] * 0.01
    data[5] = data[5] * 0.01
    # TODO 将十合一传感器数据保存至数据库
    env_data = EnvData(
        eco2=data[0],
        tvoc=data[1],
        ch2o=data[2],
        pm2_5=data[3],
        humi=data[4],
        temp=data[5],
        pm10=data[6],
        pm1=data[7],
        illu=data[8],
        mcu_temp=data[9],
        noise=data[10],
        create_time=timezone.now()
    )
    env_data.save()
    # TODO 判断当前温度和光照数据与任务书中给出的阈值的关系，开启或关闭对应设备
    conn2 = ModbusTcpUtils.get_conn2()
    if data[4] > 25:
        conn2.execute(1, cst.WRITE_SINGLE_COIL, 5, 1, 1)
    else:
        conn2.execute(1, cst.WRITE_SINGLE_COIL, 5, 1, 0)
    if data[8] < 500:
        conn2.execute(1, cst.WRITE_SINGLE_COIL, 4, 1, 1)
    else:
        conn2.execute(1, cst.WRITE_SINGLE_COIL, 4, 1, 0)
    return HttpResponse(json.dumps(data))
