import json

from django.http import HttpResponse
from django.shortcuts import render

from utils.modbusTcpUtils import ModbusTcpUtils
import modbus_tk.defines as cst


# Create your views here.
def to_sub03(request):
    return render(request, "task3.html")


def get_data(request):
    conn = ModbusTcpUtils.get_conn3()
    # TODO 获取传送带状态，并将变量命名为data
    data = conn.execute(1, cst.READ_DISCRETE_INPUTS, 0, 2)
    return HttpResponse(json.dumps(data))


def set_data(request):
    conn = ModbusTcpUtils.get_conn3()
    # TODO 获取前端传递的控制参数，需要将获取到的控制参数转换为int型的列表
    flag = request.POST.getlist('flag[]')
    flag = list(map(int, flag))
    # TODO 根据控制参数，控制传送带状态
    conn.execute(1, cst.WRITE_MULTIPLE_COILS, 0, len(flag), flag)

    return HttpResponse(json.dumps({}))
