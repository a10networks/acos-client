#!/usr/bin/env python

# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import random
import sys
import traceback

sys.path.append(".")

import acos_client

instances = {
    # '2.7.2': {
    #     'host': '10.10.100.20',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'a10',
    # },
    # '2.7.1': {
    #     'host': 'softax.a10boise.net',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'i-9276ff9f',
    # }
    '2.7.2': {
        'host': 'dougw-softax-272',
        'port': 8443,
        'protocol': 'https',
        'user': 'admin',
        'password': 'a10',
    },
    # '2.7.1': {
    #     'host': 'dougw-softax-271',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'a10',
    # }
}

partitions = {
    'p1': {
        's1': '192.168.2.244',
        'vip1': '192.168.2.240',
        'vip2': '192.168.2.239',
        'vip3': '192.168.2.238'
    },
    'p2': {
        's1': '192.168.2.234',
        'vip1': '192.168.2.230',
        'vip2': '192.168.2.229',
        'vip3': '192.168.2.228'
    },
    'shared': {
        's1': '192.168.2.254',
        'vip1': '192.168.2.250',
        'vip2': '192.168.2.249',
        'vip3': '192.168.2.248'
    }
}


def get_client(h, password=None):
    p = password or h['password']
    c = acos_client.Client(h['host'], acos_client.AXAPI_21, h['user'], p,
                           port=h['port'],
                           protocol=h['protocol'])
    return c


def run_all(version, ax, partition, pmap):
    print("=============================================================")
    print("=============================================================")
    print("=============================================================")
    print("=============================================================")
    print("RUNNING WITH ACOS VERSION ", version)

    print("=============================================================")
    print("")
    print("Basic login/get info twice")
    c = get_client(ax)
    c.system.information()

    print("=============================================================")
    print("")
    print("About to do an authenticate with a bad password")
    try:
        c = get_client(ax, password='badpass')
    except acos_client.errors.AuthenticationFailure:
        print("got bad auth exception, good")

    print("=============================================================")
    print("")
    print("About to do a good close")
    c = get_client(ax)
    c.session.close()

    print("=============================================================")
    print("")
    print("About to do a close with no session id")
    c = get_client(ax)
    c.session.close()
    if c.session.session_id is not None:
        print("ERROR: session id is not none")
        print("ERROR: ", c.session.session_id)
    c.session.close()

    print("=============================================================")
    print("")
    print("About to do a close with bad session id")
    c.session.session_id = 'bad_session_id'
    c.session.close()

    print("=============================================================")
    print("")
    print("About to do a get info with bad session id")
    c.session.session_id = 'bad_session_id'
    try:
        c.system.information()
    except acos_client.errors.InvalidSessionID:
        print("got invalid session error, good")

    # Get a fresh client

    c = get_client(ax)

    print("=============================================================")
    print("")
    print(" PARTITIONS!!! ")

    print("=============================================================")
    print("")
    print("About to search for partition")

    p_exists = c.system.partition.exists(partition)

    print("=============================================================")
    print("")
    print("About to make partition active (not exist, if not shared)")

    try:
        c.system.partition.active(partition)
    except acos_client.errors.NotFound:
        pass

    print("=============================================================")
    print("")
    print("About to create partition")

    if not p_exists:
        c.system.partition.create(partition)

    try:
        c.system.partition.create(partition)
    except acos_client.errors.Exists:
        pass

    print("=============================================================")
    print("")
    print("About to make partition active")

    c.system.partition.active(partition)

    print("=============================================================")
    # print("")
    # print("Write mem")
    # c = get_client(ax)
    # print("A")
    # c.system.write_memory()

    print("=============================================================")
    print("")
    print("Server Create")
    c.slb.server.delete("foobar")
    c.slb.server.create("foobar", pmap['s1'])
    c.slb.server.get("foobar")
    try:
        c.slb.server.create("foobar", pmap['s1'])
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.server.delete("foobar")
    c.slb.server.delete("foobar")
    try:
        c.slb.server.get("foobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.server.create("foobar", pmap['s1'])

    print("=============================================================")
    print("")
    print("SG Create")
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.ROUND_ROBIN)
    c.slb.service_group.get("pfoobar")
    try:
        c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                                   c.slb.service_group.ROUND_ROBIN)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.service_group.update("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.LEAST_CONNECTION)
    try:
        c.slb.service_group.update("pnfoobar", c.slb.service_group.TCP,
                                   c.slb.service_group.LEAST_CONNECTION)
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.delete("pfoobar")
    try:
        c.slb.service_group.get("pfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.ROUND_ROBIN)

    print("=============================================================")
    print("")
    print("VIP Create")
    c.slb.virtual_server.delete("vip3")
    c.slb.virtual_server.create("vip3", pmap['vip3'])
    c.slb.virtual_server.get("vip3")

    c.slb.virtual_server.delete("vfoobar")
    c.slb.virtual_server.create("vfoobar", pmap['vip1'])
    c.slb.virtual_server.get("vfoobar")
    try:
        c.slb.virtual_server.create("vfoobar", pmap['vip1'])
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.virtual_server.stats("vfoobar")
    c.slb.virtual_server.delete("vfoobar")
    c.slb.virtual_server.delete("vfoobar")
    try:
        c.slb.virtual_server.get("vfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")

    c.slb.virtual_server.vport.delete("vip3", "vip3_VPORT",
                                      c.slb.virtual_server.vport.HTTP, 80)
    c.slb.virtual_server.vport.create("vip3", "vip3_VPORT",
                                      service_group_name="pfoobar",
                                      protocol=c.slb.virtual_server.vport.HTTP,
                                      port='80')
    try:
        c.slb.virtual_server.vport.create(
            "vip3", "vip3_VPORT",
            service_group_name="pfoobar",
            protocol=c.slb.virtual_server.vport.HTTP,
            port='80')
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.virtual_server.vport.delete("vip3", "vip3_VPORT",
                                      c.slb.virtual_server.vport.HTTP, 80)
    c.slb.virtual_server.vport.delete("vip3", "vip3_VPORT",
                                      c.slb.virtual_server.vport.HTTP, 80)

    print("=============================================================")
    print("")
    print("HM Create")
    c.slb.hm.delete("hfoobar")
    c.slb.hm.create("hfoobar", c.slb.hm.HTTP, 5, 5, 5, 'GET', '/', '200', 80)
    c.slb.hm.get("hfoobar")
    try:
        c.slb.hm.create("hfoobar", c.slb.hm.HTTP, 5, 5, 5, 'GET', '/', '200',
                        80)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.hm.update("hfoobar", c.slb.hm.HTTP, 10, 10, 10)
    try:
        c.slb.hm.update("hnfoobar", c.slb.hm.HTTP, 10, 10, 10)
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.hm.delete("hfoobar")
    c.slb.hm.delete("hfoobar")
    try:
        c.slb.hm.get("hfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")

    print("=============================================================")
    print("")
    print("Member Create")
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
    c.slb.service_group.member.create("pfoobar", "foobar", 80)
    try:
        c.slb.service_group.member.create("pfoobar", "foobar", 80)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.service_group.member.update("pfoobar", "foobar", 80,
                                      c.slb.DOWN)
    try:
        c.slb.service_group.member.update("pfoobar", "nfoobar", 80)
    except acos_client.errors.NotFound:
        print("got not found, good")
    try:
        c.slb.service_group.member.update("pnfoobar", "foobar", 80)
    except acos_client.errors.NoSuchServiceGroup:
        print("got not found, good")
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)

    print("=============================================================")
    print("")
    print("Source Ip Persistence")
    c.slb.template.src_ip_persistence.delete("sip1")
    c.slb.template.src_ip_persistence.create("sip1")
    try:
        c.slb.template.src_ip_persistence.create("sip1")
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.template.src_ip_persistence.get("sip1")
    c.slb.template.src_ip_persistence.exists("sip1")
    c.slb.template.src_ip_persistence.delete("sip1")
    c.slb.template.src_ip_persistence.delete("sip1")
    try:
        c.slb.template.src_ip_persistence.get("sip1")
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.template.src_ip_persistence.create("sip1")

    print("=============================================================")
    print("")
    print("Http Cookie Persistence")
    c.slb.template.cookie_persistence.delete("cp1")
    c.slb.template.cookie_persistence.create("cp1")
    try:
        c.slb.template.cookie_persistence.create("cp1")
    except acos_client.errors.Exists:
        print("got already exists error, good")
    c.slb.template.cookie_persistence.get("cp1")
    c.slb.template.cookie_persistence.exists("cp1")
    c.slb.template.cookie_persistence.delete("cp1")
    c.slb.template.cookie_persistence.delete("cp1")
    try:
        c.slb.template.cookie_persistence.get("cp1")
    except acos_client.errors.NotFound:
        print("got not found, good")
    c.slb.template.cookie_persistence.create("cp1")

    print("=============================================================")
    print("")
    print("Vip with pers")
    c.slb.virtual_server.delete("vip2")
    c.slb.virtual_server.create("vip2", pmap['vip2'])
    c.slb.virtual_server.vport.create(
        "vip2", "vip2_vport1",
        protocol=c.slb.virtual_server.vport.HTTPS,
        port=443,
        service_group_name='pfoobar',
        s_pers_name='sip1',
        c_pers_name='cp1',
        status=1)
    c.slb.virtual_server.vport.create(
        "vip2", "vip2_vport2",
        protocol=c.slb.virtual_server.vport.HTTPS,
        port=444,
        service_group_name='pfoobar',
        s_pers_name='sip1')
    c.slb.virtual_server.vport.create(
        "vip2", "vip2_vport3",
        protocol=c.slb.virtual_server.vport.HTTPS,
        port=445,
        service_group_name='pfoobar',
        c_pers_name='cp1')

    print("=============================================================")
    print("")
    print("About half the time, delete the partition!")

    if int(random.random() * 2):
        c.system.partition.delete(partition)
        try:
            c.system.partition.delete(partition)
        except acos_client.errors.NotFound:
            pass


for partition, v in partitions.items():
    for version, ax in instances.items():
        try:
            run_all(version, ax, partition, v)
        except Exception as e:
            traceback.print_exc()
            print(e)
            sys.exit(1)

sys.exit(0)
