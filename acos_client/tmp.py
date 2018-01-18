# -*- coding: utf-8 -*-

__author__ = 'wenjiexu'
# @Time    : 18-1-17 下午8:34
# @File    : tmp.py.py
# @Description :

import acos_client as acos
c = acos.Client('10.5.36.4', acos.AXAPI_30, 'opsadmin', 'md7jrH7eH<Qkzoi2i4uv', port=80, protocol='http')
c.partition.active("L3V-GW02")

c.devicecontext.switch_context(2)
print c.network.vlan.get_all()
