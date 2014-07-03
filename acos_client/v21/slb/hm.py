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

import acos_client.errors as acos_errors
import acos_client.v21.base as base


class HealthMonitor(base.BaseV21):

    def get(self, name):
        return self.http.post(self.url("slb.server.search"),
                              {'name': name})

    def create(self, name, ip_address):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
            }
        }
        self.http.post(self.url("slb.server.create"), params)


    def delete(self, name):
        self.http.post(self.url("slb.server.delete"),
                       {"server": {"name": name}})

ICMP_HM_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&"
                        "method=slb.hm.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format="
                        "json&method=slb.hm.update&"
                        "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format="
                        "json&method=slb.hm.delete&session_id=%s"}
             },
    "ds": {
        'retry': 3,
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 0,
    }
}))

TCP_HM_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&"
                        "method=slb.hm.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format="
                        "json&method=slb.hm.update&"
                        "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format="
                        "json&method=slb.hm.delete&session_id=%s"}
             },
    "ds": {
        'retry': 3,
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 1,
    }
}))

HTTP_HM_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.hm.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format="
                                "json&method=slb.hm.update&"
                                "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format="
                                "json&method=slb.hm.delete&session_id=%s"}
             },
    "ds": {
        'retry': 3,
        'http': {
            'port': 80,
            'url': u'GET /foo',
            'expect_code': u'200'
        },
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 3,
    }
}))

HTTPS_HM_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.hm.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?"
                                "format=json&method=slb.hm.update&"
                                "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.hm.delete&session_id=%s"}
             },
    "ds": {
        'retry': 3,
        'https': {
            'url': 'GET /foo',
            'port': 80,
            'expect_code': '200'
        },
        'name': 'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 4,
    }
}))


    def _health_monitor_set(self, request_struct_root, mon_type, name,
                            interval, timeout, max_retries,
                            method=None, url=None, expect_code=None):

        hm_req = request_struct_root.toDict().items()
        if mon_type == 'TCP':
            hm_obj = request_struct_v2.TCP_HM_OBJ.ds.toDict()
        elif mon_type == 'PING':
            hm_obj = request_struct_v2.ICMP_HM_OBJ.ds.toDict()
        elif mon_type == 'HTTP':
            hm_obj = request_struct_v2.HTTP_HM_OBJ.ds.toDict()
        elif mon_type == 'HTTPS':
            hm_obj = request_struct_v2.HTTPS_HM_OBJ.ds.toDict()
        else:
            raise a10_ex.HealthMonitorUpdateError(hm=name)

        hm_obj['name'] = name
        hm_obj['interval'] = interval
        hm_obj['timeout'] = timeout
        hm_obj['consec_pass_reqd'] = max_retries

        mt = mon_type.lower()
        hm_obj[mt]['url'] = "%s %s" % (method, url)
        hm_obj[mt]['expect_code'] = expect_code

        r = self.send(tenant_id=self.tenant_id,
                      method=hm_req[0][0],
                      url=hm_req[0][1],
                      body=hm_obj)

        if self.inspect_response(r) is not True:
            raise a10_ex.HealthMonitorUpdateError(hm=name)


    def health_monitor_create(self, mon_type, name,
                              interval, timeout, max_retries,
                              method=None, url=None, expect_code=None):
        self._health_monitor_set(request_struct_v2.TCP_HM_OBJ.call.create,
                                 mon_type, name,
                                 interval, timeout, max_retries,
                                 method, url, expect_code)

    def health_monitor_update(self, mon_type, name,
                              interval, timeout, max_retries,
                              method=None, url=None, expect_code=None):
        self._health_monitor_set(request_struct_v2.TCP_HM_OBJ.call.update,
                                 mon_type, name,
                                 interval, timeout, max_retries,
                                 method, url, expect_code)

    def health_monitor_delete(self, healthmon_id):
        hm_del_req = (request_struct_v2.HTTP_HM_OBJ.call.delete
                      .toDict().items())

        r = self.send(tenant_id=self.tenant_id,
                      method=hm_del_req[0][0],
                      url=hm_del_req[0][1],
                      body={"name": healthmon_id})

        if self.inspect_response(r, func='delete') is not True:
            raise a10_ex.HealthMonitorDeleteError(hm=healthmon_id)
