#!/usr/bin/env python

import sys
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
    '2.7.1': {
        'host': 'dougw-softax-271',
        'port': 8443,
        'protocol': 'https',
        'user': 'admin', 
        'password': 'a10',
    }
}

def get_client(h, password=None):
    p = password or h['password']
    c = acos_client.Client(h['host'], h['user'], p,
                           port=h['port'],
                           protocol=h['protocol'])
    #c.system.information()
    return c


for version,ax in instances.items():
    print "============================================================="
    print "============================================================="
    print "============================================================="
    print "============================================================="
    print "RUNNING WITH ACOS VERSION ", version

    print "============================================================="
    print ""
    print "Basic login/get info twice"
    c = get_client(ax)
    c.system.information()

    print "============================================================="
    print ""
    print "About to do an authenticate with a bad password"
    try:
        c = get_client(ax, password='badpass')
    except acos_client.errors.AuthenticationFailure:
        print "got bad auth exception, good"

    print "============================================================="
    print ""
    print "About to do a good close"
    c = get_client(ax)
    c.session.close()

    print "============================================================="
    print ""
    print "About to do a close with no session id"
    c = get_client(ax)
    c.session.close()
    if c.session.session_id is not None:
        print "ERROR: session id is not none"
        print "ERROR: ", c.session.session_id
    c.session.close()

    print "============================================================="
    print ""
    print "About to do a close with bad session id"
    c.session.session_id = 'bad_session_id'
    c.session.close()

    print "============================================================="
    print ""
    print "About to do a get info with bad session id"
    c.session.session_id = 'bad_session_id'
    try:
        c.system.information()
    except acos_client.errors.InvalidSessionID:
        print "got invalid session error, good"

    print "============================================================="
    # print ""
    # print "Write mem"
    # c = get_client(ax)
    # print "A"
    # c.system.write_memory()

    print "============================================================="
    print ""
    print "Server Create"
    c = get_client(ax)
    c.slb.server.delete("foobar")
    c.slb.server.create("foobar", "192.168.2.254")
    c.slb.server.get("foobar")
    try:
        c.slb.server.create("foobar", "192.168.2.254")
    except acos_client.errors.Exists:
        print "got already exists error, good"
    c.slb.server.delete("foobar")
    c.slb.server.delete("foobar")
    try:
        c.slb.server.get("foobar")
    except acos_client.errors.NotFound:
        print "got not found, good"
    c.slb.server.create("foobar", "192.168.2.254")


    print "============================================================="
    print ""
    print "SG Create"
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.ROUND_ROBIN)
    c.slb.service_group.get("pfoobar")
    try:
        c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                                   c.slb.service_group.ROUND_ROBIN)
    except acos_client.errors.Exists:
        print "got already exists error, good"
    c.slb.service_group.delete("pfoobar")
    c.slb.service_group.delete("pfoobar")
    try:
        c.slb.service_group.get("pfoobar")
    except acos_client.errors.NotFound:
        print "got not found, good"
    c.slb.service_group.create("pfoobar", c.slb.service_group.TCP,
                               c.slb.service_group.ROUND_ROBIN)


    print "============================================================="
    print ""
    print "VIP Create"
    c.slb.virtual_server.delete("vfoobar")
    c.slb.virtual_server.create("vfoobar", 
                                '192.168.2.250',
                                c.slb.virtual_service.HTTP,
                                '80',
                                'pfoobar')
    c.slb.virtual_server.get("vfoobar")
    try:
        c.slb.virtual_server.create("vfoobar", 
                                    '192.168.2.250',
                                    c.slb.virtual_service.HTTP,
                                    '80',
                                    'pfoobar')
    except acos_client.errors.Exists:
        print "got already exists error, good"
    c.slb.virtual_server.delete("vfoobar")
    c.slb.virtual_server.delete("vfoobar")
    try:
        c.slb.virtual_server.get("vfoobar")
    except acos_client.errors.NotFound:
        print "got not found, good"


    print "============================================================="
    print ""
    print "HM Create"
    c.slb.hm.delete("hfoobar")
    c.slb.hm.create(c.slb.hm.HTTP, "hfoobar", 5, 5, 5, 'GET', '/', '200', 80)
    c.slb.hm.get("hfoobar")
    try:
        c.slb.hm.create(c.slb.hm.HTTP, "hfoobar", 5, 5, 5, 'GET', '/', '200', 80)
    except acos_client.errors.Exists:
        print "got already exists error, good"
    c.slb.hm.delete("hfoobar")
    c.slb.hm.delete("hfoobar")
    try:
        c.slb.hm.get("hfoobar")
    except acos_client.errors.NotFound:
        print "got not found, good"


    print "============================================================="
    print ""
    print "Member Create"
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
    c.slb.service_group.member.create("pfoobar", "foobar", 80)
    try:
        c.slb.service_group.member.create("pfoobar", "foobar", 80)
    except acos_client.errors.Exists:
        print "got already exists error, good"
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
    c.slb.service_group.member.delete("pfoobar", "foobar", 80)
