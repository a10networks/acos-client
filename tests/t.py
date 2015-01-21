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
    #     'axapi': '21',
    # },
    # '2.7.1': {
    #     'host': 'softax.a10boise.net',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'i-9276ff9f',
    #     'axapi': '21',
    # }
    # '2.7.2': {
    #     'host': 'dougw-softax-272',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'a10',
    #     'axapi': '21',
    # },
    # '2.7.1': {
    #     'host': 'dougw-softax-271',
    #     'port': 8443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'a10',
    #     'axapi': '21',
    # },
    # '4.0.0': {
    #     'host': 'dougw-softax-4',
    #     'port': 443,
    #     'protocol': 'https',
    #     'user': 'admin',
    #     'password': 'a10',
    #     'axapi': '30',
    # },
    '4.0.0': {
        'host': '172.18.61.29',
        'port': 443,
        'protocol': 'https',
        'user': 'admin',
        'password': 'a10',
        'axapi': '30',
    },
}

partitions = [
    {
        'name': 'shared',
        's1': '192.168.2.254',
        'vip1': '192.168.2.250',
        'vip2': '192.168.2.249',
        'vip3': '192.168.2.248'
    },
    {
        'name': 'p1',
        's1': '192.168.2.244',
        'vip1': '192.168.2.240',
        'vip2': '192.168.2.239',
        'vip3': '192.168.2.238'
    },
    {
        'name': 'p2',
        's1': '192.168.2.234',
        'vip1': '192.168.2.230',
        'vip2': '192.168.2.229',
        'vip3': '192.168.2.228'
    },
]


class Nope(Exception):
    pass


def get_client(h, password=None):
    p = password or h['password']
    c = acos_client.Client(h['host'], h['axapi'], h['user'], p,
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
    r = c.system.information()
    print("LIBRARY RESPONSE = %s", r)

    print("=============================================================")
    print("")
    print("About to do an authenticate with a bad password")
    try:
        c = get_client(ax, password='badpass')
        c.system.information()
    except acos_client.errors.AuthenticationFailure:
        print("got bad auth exception, good")
    else:
        sys.stdout.flush()
        raise Nope()

    print("=============================================================")
    print("")
    print("About to do a good close")
    c = get_client(ax)
    c.system.information()
    c.session.close()

    print("=============================================================")
    print("")
    print("About to do a close with no session id")
    c = get_client(ax)
    c.session.close()
    if c.session.session_id is not None:
        print("ERROR: session id is not none")
        print("ERROR: ", c.session.session_id)
        raise Nope()
    print("here comes the close with no id...")
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
    else:
        raise Nope()

    # Get a fresh client

    c = get_client(ax)
    c.system.information()

    # c.ha.sync('172.18.61.27', 'admin', 'a10')

    print("=============================================================")
    print("")
    print(" PARTITIONS!!! ")

    print("=============================================================")
    print("")
    print("About to search for partition")

    p_exists = c.system.partition.exists(partition)
    print("LIBRARY RESPONSE = %s", p_exists)

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
    print("")
    print("Write mem")
    c = get_client(ax)
    print("A")
    c.system.action.write_memory()

    # print("=============================================================")
    # print("")
    # print("Client SSL Create")
    # c.slb.template.client_ssl.delete("ss1")
    # c.slb.template.client_ssl.create("ss1", "cert1", "cert1")
    # c.slb.template.client_ssl.get("ss1")
    # try:
    #     c.slb.template.client_ssl.create("ss1", "cert1", "cert1")
    # except acos_client.errors.Exists:
    #     print("got already exists error, good")
    # c.slb.template.client_ssl.update("ss1", "cert1", "cert1")
    # try:
    #     c.slb.template.client_ssl.update("sns1", "cert1", "cert1")

    # except acos_client.errors.NotFound:
    #     print("got not found, good")
    # c.slb.template.client_ssl.delete("ss1")
    # c.slb.template.client_ssl.delete("ss1")
    # try:
    #     c.slb.template.client_ssl.get("ss1")
    # except acos_client.errors.NotFound:
    #     print("got not found, good")
    # c.slb.template.client_ssl.create("ss1", "cert1", "cert1")

    # print("=============================================================")
    # print("")
    # print("Server SSL Create")
    # c.slb.template.server_ssl.delete("ss1")
    # c.slb.template.server_ssl.create("ss1", "cert1", "cert1")
    # c.slb.template.server_ssl.get("ss1")
    # try:
    #     c.slb.template.server_ssl.create("ss1", "cert1", "cert1")
    # except acos_client.errors.Exists:
    #     print("got already exists error, good")
    # c.slb.template.server_ssl.update("ss1", "cert1", "cert1")
    # try:
    #     c.slb.template.server_ssl.update("sns1", "cert1", "cert1")
    # except acos_client.errors.NotFound:
    #     print("got not found, good")
    # c.slb.template.server_ssl.delete("ss1")
    # c.slb.template.server_ssl.delete("ss1")
    # try:
    #     c.slb.template.server_ssl.get("ss1")
    # except acos_client.errors.NotFound:
    #     print("got not found, good")
    # c.slb.template.server_ssl.create("ss1", "cert1", "cert1")

    print("=============================================================")
    print("")
    print("Server Create")
    c.slb.server.delete("foobar")
    c.slb.server.create("foobar", pmap['s1'])
    r = c.slb.server.get("foobar")
    print("LIBRARY RESPONSE = %s", r)
    try:
        c.slb.server.create("foobar", pmap['s1'])
    except acos_client.errors.Exists:
        print("got already exists error, good")
    else:
        raise Nope()
    c.slb.server.delete("foobar")
    c.slb.server.delete("foobar")
    try:
        c.slb.server.get("foobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
    c.slb.server.create("foobar", pmap['s1'])

    print("=============================================================")
    print("")
    print("SG Create")
    # temp -- odd that we have to delete this vport
    c.slb.virtual_server.vport.delete(
        "vip3", "vip3_VPORT", c.slb.virtual_server.vport.HTTP, 80)
    # temp -- odd that we have to delete this vport
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.ROUND_ROBIN)
    r = c.slb.service_group.get("pfoobar")
    print("LIBRARY RESPONSE = %s", r)
    try:
        c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                                   c.slb.service_group.ROUND_ROBIN)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    else:
        raise Nope()
    c.slb.service_group.update("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.LEAST_CONNECTION)
    try:
        c.slb.service_group.update("pnfoobar", c.slb.service_group.TCP,
                                   c.slb.service_group.LEAST_CONNECTION)
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.delete("pfoobar")
    try:
        c.slb.service_group.get("pfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
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
    r = c.slb.virtual_server.get("vfoobar")
    print("LIBRARY RESPONSE = %s", r)
    r = c.slb.virtual_server.all()
    print("LIBRARY RESPONSE = %s", r)
    try:
        c.slb.virtual_server.create("vfoobar", pmap['vip1'])
    except acos_client.errors.Exists:
        print("got already exists error, good")
    else:
        raise Nope()
    try:
        c.slb.virtual_server.stats("vfoobar")
    except Exception:
        pass
    c.slb.virtual_server.delete("vfoobar")
    c.slb.virtual_server.delete("vfoobar")
    try:
        c.slb.virtual_server.get("vfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()

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
    else:
        raise Nope()
    c.slb.virtual_server.vport.delete("vip3", "vip3_VPORT",
                                      c.slb.virtual_server.vport.HTTP, 80)
    c.slb.virtual_server.vport.delete("vip3", "vip3_VPORT",
                                      c.slb.virtual_server.vport.HTTP, 80)

    print("=============================================================")
    print("")
    print("HM Create")
    c.slb.hm.delete("hnfoobar")
    c.slb.hm.delete("hfoobar")
    c.slb.hm.create("hfoobar", c.slb.hm.HTTP, 5, 5, 5, 'GET', '/', '200', 80)
    r = c.slb.hm.get("hfoobar")
    print("LIBRARY RESPONSE = %s", r)
    try:
        c.slb.hm.create("hfoobar", c.slb.hm.HTTP, 5, 5, 5, 'GET', '/', '200',
                        80)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    else:
        raise Nope()
    c.slb.hm.update("hfoobar", c.slb.hm.HTTP, 10, 10, 10)
    try:
        c.slb.hm.update("hnfoobar", c.slb.hm.HTTP, 10, 10, 10)
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
    c.slb.hm.delete("hfoobar")
    c.slb.hm.delete("hfoobar")
    try:
        c.slb.hm.get("hfoobar")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()

    c.slb.hm.delete("hm2")
    c.slb.hm.create("hm2", c.slb.hm.ICMP, 5, 5, 5)
    r = c.slb.hm.get("hm2")

    c.slb.hm.delete("hm4")
    c.slb.hm.create("hm4", c.slb.hm.TCP, 5, 5, 5, port=25)
    r = c.slb.hm.get("hm4")

    c.slb.hm.delete("hm3")
    c.slb.hm.create("hm3", c.slb.hm.HTTPS, 5, 5, 5, 'GET', '/', '200', 443)
    r = c.slb.hm.get("hm3")

    print("=============================================================")
    print("")
    print("Member Create")
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
    c.slb.service_group.member.create("pfoobar", "foobar", 80)
    try:
        c.slb.service_group.member.create("pfoobar", "foobar", 80)
    except acos_client.errors.Exists:
        print("got already exists error, good")
    else:
        raise Nope()
    c.slb.service_group.member.update("pfoobar", "foobar", 80,
                                      c.slb.DOWN)
    try:
        c.slb.service_group.member.update("pfoobar", "nfoobar", 80)
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
    try:
        c.slb.service_group.member.update("pnfoobar", "foobar", 80)
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
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
    else:
        raise Nope()
    r = c.slb.template.src_ip_persistence.get("sip1")
    print("LIBRARY RESPONSE = %s", r)
    c.slb.template.src_ip_persistence.exists("sip1")
    c.slb.template.src_ip_persistence.delete("sip1")
    c.slb.template.src_ip_persistence.delete("sip1")
    try:
        c.slb.template.src_ip_persistence.get("sip1")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
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
    else:
        raise Nope()
    c.slb.template.cookie_persistence.get("cp1")
    c.slb.template.cookie_persistence.exists("cp1")
    c.slb.template.cookie_persistence.delete("cp1")
    c.slb.template.cookie_persistence.delete("cp1")
    try:
        c.slb.template.cookie_persistence.get("cp1")
    except acos_client.errors.NotFound:
        print("got not found, good")
    else:
        raise Nope()
    c.slb.template.cookie_persistence.create("cp1")

    print("=============================================================")
    print("")
    print("Vip with pers")
    c.slb.virtual_server.delete("vip2")
    c.slb.virtual_server.create("vip2", pmap['vip2'])
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

    c.session.close()


def main():
    for v in partitions:
        partition = v['name']
        for version, ax in instances.items():
            try:
                run_all(version, ax, partition, v)
            except Exception as e:
                traceback.print_exc()
                print(e)
                sys.exit(1)
    # for version, ax in instances.items():
    #     try:
    #         run_all(version, ax, 'shared', partitions['shared'])
    #     except Exception as e:
    #         traceback.print_exc()
    #         print(e)
    #         sys.exit(1)

if __name__ == '__main__':
    main()
    sys.exit(0)
