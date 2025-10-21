# TODO 01.引入Modbus相关工具包
from modbus_tk import modbus_tcp
import modbus_tk.defines as cst


class ModbusTcpUtils:

    _conn1 = None
    _conn2 = None
    _conn3 = None

    @classmethod
    def get_conn1(cls):
        if cls._conn1 == None:
            # TODO 替换pass语句，创建到十合一空气质量传感器的ModbusTcp链接，赋值给_conn1
            cls._conn1 = modbus_tcp.TcpMaster(host='192.168.1.6', port=26)
        return cls._conn1

    @classmethod
    def get_conn2(cls):
        if cls._conn2 == None:
            # TODO  替换pass语句，创建到控制照明灯与排风扇等设备的艾莫迅串口服务器的ModbusTcp链接，赋值给_conn2
            cls._conn2 = modbus_tcp.TcpMaster(host='192.168.1.13', port=502)
        return cls._conn2

    @classmethod
    def get_conn3(cls):
        if cls._conn3 == None:
            # TODO  替换pass语句，创建到控制传送带设备的串口服务器的ModbusTcp链接，赋值给_conn3
            cls._conn3 = modbus_tcp.TcpMaster(host='192.168.1.12', port=502)
        return cls._conn3
