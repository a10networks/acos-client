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

import json

import mock
import unittest

import acos_client

DEFAULT_SESSION_ID = 'session0'


class MockPairClient(object):

    def __init__(self, parent, session_id=None):
        self.parent = parent
        self.session_id = session_id

    def __enter__(self):
        c = acos_client.Client('localhost', acos_client.AXAPI_21,
                               self.parent.username,
                               self.parent.password)
        c.http._http = self.parent.mock()
        c.session.http._http = c.http._http
        if self.session_id is not None:
            c.session.session_id = self.session_id

        return c

    def __exit__(self, *args, **kwargs):
        self.parent.post_validate()


class MockPair(unittest.TestCase):
    method = 'POST'
    action = None
    params = None
    response = None

    def __init__(self, fields={}):
        self.testMethodPrefix = "DONTRUNME"
        self.fields = fields
        self.session_id = fields.get('session_id', 'session0')
        self.username = fields.get('username', 'defuser')
        self.password = fields.get('password', 'defpass')

    def url(self, session_id=None):
        return ("/services/rest/v2.1/?format=json&method=%s&session_id=%s" %
                (self.action, session_id))

    def client(self, session_id=None):
        self._client = MockPairClient(self, session_id=session_id)
        return self._client

    def mock(self):
        self._mock = mock.MagicMock(return_value=json.dumps(self.output()))
        return self._mock

    def output(self):
        if self.response is not None:
            return self.response
        else:
            return

    def post_validate(self):
        if self.action is not None:
            validated = False
            if self.params is not None:
                for name, args, kwargs in self._mock.mock_calls:
                    if args and len(args) > 2 and args[2].__class__ == str:
                        print("json = %s" % args[2])
                        if json.loads(args[2]) == self.params:
                            validated = True
                    else:
                        validated = True
            else:
                validated = True
            print("params = %s" % self.params)
            self.assertTrue(validated)


class AuthenticatedMockPair(MockPair):
    response = {"response": {"status": "OK"}}

    def client(self):
        return super(AuthenticatedMockPair, self).client(
            session_id=self.session_id)


class Session(MockPair):

    def output(self):
        return {'session_id': self.session_id}

    def post_validate(self):
        self._mock.assert_called_once_with(
            'POST',
            '/services/rest/v2.1/?format=json&method=authenticate',
            json.dumps({'username': self.username, 'password': self.password}))


class SessionBadPassword(Session):

    def output(self):
        return {
            "response": {
                "status": "fail",
                "err": {"code": 520486915, "msg": " Admin password error"}
            }
        }


class Close(AuthenticatedMockPair):
    action = 'session.close'
    params = {'session_id': DEFAULT_SESSION_ID}


class CloseBadSession(Close):
    params = {'session_id': "badsessionid"}
    response = {
        "response": {
            "status": "fail",
            "err": {"code": 1009, "msg": "Invalid session ID"}
        }
    }


class SystemInformation(AuthenticatedMockPair):
    method = 'GET'
    action = 'system.information.get'
    params = {}
    response = {
        'system_information': {
            'advanced_core_os_on_compact_flash1': 'No Software',
            'advanced_core_os_on_compact_flash2': 'No Software',
            'advanced_core_os_on_harddisk1': '2.7.1-P3-AWS(build: 4)',
            'advanced_core_os_on_harddisk2': '2.7.1-P3-AWS(build: 4)',
            'aflex_engine_version': '2.0.0',
            'axapi_version': '2.1',
            'current_time': '03:25:47 IST Tue Jul 1 2014',
            'firmware_version': 'N/A',
            'last_config_saved': '06:25:26 GMT Sat Dec 28 2013',
            'serial_number': 'N/A',
            'software_version': '2.7.1-P3-AWS(build: 4)',
            'startup_mode': 'hard disk primary',
            'technical_support': 'www.a10networks.com/support '
        }
    }


class SystemWriteMemory(AuthenticatedMockPair):
    method = 'GET'
    action = 'system.action.write_memory'
    params = {}


class Server(AuthenticatedMockPair):
    params = {'name': 's1'}


class ServerDelete(Server):
    action = 'slb.server.delete'
    params = {"server": {"name": 's1'}}


class ServerDeleteNotFound(ServerDelete):
    response = {
        "response": {
            "status": "fail",
            "err": {
                "code": 67174402,
                "msg": " No such Server"}
        }
    }


class ServerCreate(Server):
    action = 'slb.server.create'
    params = {'server': {'host': '192.168.2.254', "status": 1, 'name': 's1'}}


class ServerCreateExists(ServerCreate):
    response = {"response": {"status": "fail", "err": {"code": 402653200,
                "msg": " Name or IP address already exists."}}}


class ServerSearch(Server):
    action = 'slb.server.search'
    response = {
        'server': {
            'status': 1, 'conn_resume': 0, 'weight': 1,
            'conn_limit': 8000000, 'host': '192.168.2.254',
            'spoofing_cache': 0, 'port_list': [],
            'gslb_external_address': '0.0.0.0', 'slow_start': 0,
            'name': 's1', 'health_monitor': '(default)',
            'extended_stats': 0, 'template': 'default', 'stats_data': 1,
            'conn_limit_log': 0
        }
    }


class ServerSearchNotFound(ServerSearch):
    response = {"response": {"status": "fail", "err": {"code": 67174402,
                "msg": " No such Server"}}}


class ServiceGroup(AuthenticatedMockPair):
    params = {'name': 'pool1'}


class ServiceGroupDelete(ServiceGroup):
    action = 'slb.service_group.delete'


class ServiceGroupDeleteNotFound(ServiceGroupDelete):
    response = {"response": {"status": "fail", "err": {"code": 67305473,
                "msg": " No such service group"}}}


class ServiceGroupCreate(ServiceGroup):
    action = 'slb.service_group.create'
    params = {'service_group': {'lb_method': 0, 'protocol': 2,
              'name': 'pool1'}}


class ServiceGroupCreateExists(ServiceGroupCreate):
    response = {"response": {"status": "fail", "err": {"code": 402653201,
                "msg": " Service group already exists."}}}


class ServiceGroupSearch(ServiceGroup):
    action = 'slb.service_group.search'
    response = {
        'service_group': {
            'lb_method': 0,
            'protocol': 2,
            'name': 'pool1',
            'backup_server_event_log_enable': 0,
            'health_monitor': '',
            'client_reset': 0,
            'min_active_member': {
                'status': 0,
                'number': 0,
                'priority_set': 0
            },
            'extended_stats': 0,
            'stats_data': 1,
            'member_list': []
        }
    }


class ServiceGroupSearchNotFound(ServiceGroupSearch):
    response = {"response": {"status": "fail", "err": {"code": 67305473,
                "msg": " No such service group"}}}


class ServiceGroupUpdate(ServiceGroup):
    action = 'slb.service_group.update'
    params = {"service_group": {"lb_method": 2, "name": "pool1"}}


class ServiceGroupUpdateNotFound(ServiceGroupUpdate):
    response = {"response": {"status": "fail", "err": {"code": 67305473,
                "msg": " No such service group"}}}


class VirtualServer(AuthenticatedMockPair):
    params = {'name': 'vip1'}


class VirtualServerDelete(VirtualServer):
    action = 'slb.virtual_server.delete'


class VirtualServerDeleteNotFound(VirtualServerDelete):
    response = {"response": {"status": "fail", "err": {"code": 67239937,
                "msg": " No such Virtual Server"}}}


class VirtualServerCreate(VirtualServer):
    action = 'slb.virtual_server.create'
    params = {'virtual_server': {'status': 1, 'name': 'vip1',
              'address': '192.168.2.250'}}


class VirtualServerCreateExists(VirtualServerCreate):
    response = {"response": {"status": "fail", "err": {"code": 402653206,
                "msg": " Name already exists."}}}


class VirtualServerSearch(VirtualServer):
    action = 'slb.virtual_server.search'
    response = {
        "virtual_server": {
            "name": "vip1",
            "address": "192.168.2.250",
            "status": 1,
            "vrid": 0,
            "arp_status": 1,
            "stats_data": 1,
            "extended_stats": 0,
            "disable_vserver_on_condition": 0,
            "redistribution_flagged": 0,
            "ha_group": {
                "status": 0,
                "ha_group_id": 0,
                "dynamic_server_weight": 0
            },
            "vip_template": "shared/default",
            "pbslb_template": "",
            "vport_list": []
        }
    }


class VirtualServerSearchNotFound(VirtualServerSearch):
    response = {"response": {"status": "fail", "err": {"code": 67239937,
                "msg": " No such Virtual Server"}}}


class VirtualPort(AuthenticatedMockPair):
    params = {
        'vport': {
            'protocol': 11,
            'name': 'vip1_VPORT',
            'port': 80
        },
        'name': 'vip1'
    }


class VirtualPortDelete(VirtualPort):
    action = 'slb.virtual_server.vport.delete'


class VirtualPortDeleteNotFound(VirtualPortDelete):
    response = {"response": {"status": "fail", "err": {"code": 1043,
                "msg": "Can not find the virtual server port"}}}


class VirtualPortCreate(VirtualPort):
    action = 'slb.virtual_server.vport.create'
    params = {
        'vport': {
            'service_group': 'pool1',
            'status': 1,
            'protocol': 11,
            'name': 'vip1_VPORT',
            'port': 80
        },
        'name': 'vip1'
    }


class VirtualPortCreateExists(VirtualPortCreate):
    response = {"response": {"status": "fail", "err": {"code": 1406,
                "msg": "The virtual port already exists."}}}


class HealthMonitor(AuthenticatedMockPair):
    params = {'name': 'hm1'}


class HealthMonitorDelete(HealthMonitor):
    action = 'slb.hm.delete'


class HealthMonitorDeleteNotFound(HealthMonitorDelete):
    response = {"response": {"status": "fail", "err": {"code": 33619968,
                "msg": " The monitor does not exist."}}}


class HealthMonitorCreate(HealthMonitor):
    action = 'slb.hm.create'
    params = {"retry": 5, "name": "hm1", "consec_pass_reqd": 5, "interval": 5,
              "timeout": 5, "disable_after_down": 0, "type": "HTTP"}


class HealthMonitorCreateExists(HealthMonitorCreate):
    response = {"response": {"status": "fail", "err": {"code": 2941,
                "msg": "The same health monitor name already exist."}}}


class HealthMonitorSearch(HealthMonitor):
    action = 'slb.hm.search'
    response = {
        "health_monitor": {
            "name": "hfoobar",
            "retry": 5,
            "consec_pass_reqd": 5,
            "interval": 5,
            "timeout": 5,
            "strictly_retry": 0,
            "disable_after_down": 0,
            "override_ipv4": "0.0.0.0",
            "override_ipv6": "::",
            "override_port": 0,
            "type": 3,
            "http": {
                "port": 80,
                "host": "",
                "url": "GET /",
                "user": "",
                "password": "",
                "expect_code": "200",
                "maintenance_code": ""
            }
        }
    }


class HealthMonitorSearchNotFound(HealthMonitorSearch):
    response = {"response": {"status": "fail", "err": {"code": 33619968,
                "msg": " The monitor does not exist."}}}


class HealthMonitorUpdate(HealthMonitor):
    action = 'slb.hm.update'
    params = {"retry": 5, "name": "hm1", "consec_pass_reqd": 5, "interval": 5,
              "timeout": 5, "disable_after_down": 0, "type": "HTTP"}


class HealthMonitorUpdateNotFound(HealthMonitorUpdate):
    response = {"response": {"status": "fail", "err": {"code": 33619968,
                "msg": " The monitor does not exist."}}}


class Member(AuthenticatedMockPair):
    params = {'member': {'port': 80, 'server': 's1'}, 'name': 'pool1'}


class MemberDelete(Member):
    action = 'slb.service_group.member.delete'


class MemberDeleteNotFound(MemberDelete):
    response = {"response": {"status": "fail", "err": {"code": 1023,
                "msg": "Can not find the service group member"}}}


class MemberCreate(Member):
    action = 'slb.service_group.member.create'
    params = {'member': {'status': 1, 'port': 80, 'server': 's1'},
              'name': 'pool1'}


class MemberCreateExists(MemberCreate):
    response = {"response": {"status": "fail", "err": {"code": 1405,
                "msg": "The service group member already exists."}}}


class MemberUpdate(Member):
    action = 'slb.service_group.member.update'
    params = {'member': {'status': 0, 'port': 80, 'server': 's1'},
              'name': 'pool1'}


class MemberUpdateNotFound(MemberUpdate):
    response = {"response": {"status": "fail", "err": {"code": 1023,
                "msg": "Can not find the service group member"}}}


class MemberUpdateNoSuchServiceGroup(MemberUpdate):
    response = {"response": {"status": "fail", "err": {"code": 67305473,
                "msg": " No such service group"}}}


class SourceIpPersistence(AuthenticatedMockPair):
    params = {'name': 'sip1'}


class SourceIpPersistenceDelete(SourceIpPersistence):
    action = 'slb.template.src_ip_persistence.delete'


class SourceIpPersistenceDeleteNotFound(SourceIpPersistenceDelete):
    response = {"response": {"status": "fail", "err": {"code": 67371009,
                "msg": " No such Template"}}}


class SourceIpPersistenceCreate(SourceIpPersistence):
    action = 'slb.template.src_ip_persistence.create'
    params = {'src_ip_persistence_template': {'name': 'sip1'}}


class SourceIpPersistenceCreateExists(SourceIpPersistenceCreate):
    response = {"response": {"status": "fail", "err": {"code": 402653202,
                "msg": " Template name already exists."}}}


class SourceIpPersistenceSearch(SourceIpPersistence):
    action = 'slb.template.src_ip_persistence.search'
    response = {
        "src_ip_persistence_template": {
            "name": "sip1",
            "match_type": 0,
            "match_all": 0,
            "timeout": 5,
            "no_honor_conn": 0,
            "incl_sport": 0,
            "include_dstip": 0,
            "hash_persist": 0,
            "enforce_high_priority": 0,
            "netmask": "255.255.255.255",
            "netmask6": 128
        }
    }


class SourceIpPersistenceSearchNotFound(SourceIpPersistenceSearch):
    response = {"response": {"status": "fail", "err": {"code": 67371009,
                "msg": " No such Template"}}}


class HttpCookiePersistence(AuthenticatedMockPair):
    params = {'name': 'cp1'}


class HttpCookiePersistenceDelete(HttpCookiePersistence):
    action = 'slb.template.cookie_persistence.delete'


class HttpCookiePersistenceDeleteNotFound(HttpCookiePersistenceDelete):
    response = {"response": {"status": "fail", "err": {"code": 67371009,
                "msg": " No such Template"}}}


class HttpCookiePersistenceCreate(HttpCookiePersistence):
    action = 'slb.template.cookie_persistence.create'
    params = {'cookie_persistence_template': {'name': 'cp1'}}


class HttpCookiePersistenceCreateExists(HttpCookiePersistenceCreate):
    response = {"response": {"status": "fail", "err": {"code": 402653202,
                "msg": " Template name already exists."}}}


class HttpCookiePersistenceSearch(HttpCookiePersistence):
    action = 'slb.template.cookie_persistence.search'
    response = {
        "cookie_persistence_template": {
            "name": "cp1",
            "expire_exist": 0,
            "expire": 0,
            "cookie_name": "",
            "domain": "",
            "path": "",
            "match_type": 0,
            "match_all": 0,
            "insert_always": 0,
            "dont_honor_conn": 0
        }
    }


class HttpCookiePersistenceSearchNotFound(HttpCookiePersistenceSearch):
    response = {"response": {"status": "fail", "err": {"code": 67371009,
                "msg": " No such Template"}}}


class Partition(AuthenticatedMockPair):
    params = {'name': 'p1'}


class PartitionExists(Partition):
    action = 'system.partition.search'
    response = {
        "partition": {
            "partition_id": 1,
            "name": "p1",
            "max_aflex_file": 32,
            "network_partition": 0
        }
    }


class PartitionExistsNotFound(PartitionExists):
    response = {"response": {"status": "fail", "err": {"code": 520749062,
                "msg": " Partition does not exist."}}}


class PartitionActive(Partition):
    action = 'system.partition.active'


class PartitionActiveNotFound(PartitionActive):
    response = {"response": {"status": "fail", "err": {"code": 402718800,
                "msg": " Failed to get partition."}}}


class PartitionCreate(Partition):
    action = 'system.partition.create'
    params = {'partition': {'max_aflex_file': 32, 'network_partition': 0,
              'name': 'p1'}}


class PartitionCreateExists(PartitionCreate):
    response = {"response": {"status": "fail", "err": {"code": 1982,
                "msg": "The partition already exists"}}}


class PartitionDelete(Partition):
    action = 'system.partition.delete'


class PartitionDeleteNotFound(PartitionDelete):
    response = {"response": {"status": "fail", "err": {"code": 520749062,
                "msg": " Partition does not exist."}}}


class HASync(AuthenticatedMockPair):
    action = 'ha.sync_config'
    params = {
        'ha_config_sync': {
            'peer_operation': 0,
            'destination_ip': '192.168.2.254',
            'peer_reload': 0,
            'user': 'admin',
            'auto_authentication': 0,
            'sync_all_partition': 1,
            'operation': 2,
            'password': 'a10'
        }
    }
