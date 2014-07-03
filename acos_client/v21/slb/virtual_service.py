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


class VirtualService(base.BaseV21):   # aka VirtualPort

    def get(self, name):
        vport_name = name + "_VPORT"
        return self.http.post(self.url("slb.virtual_service.search"),
                              {'name': vport_name})

    def virtual_port_update(self, name, protocol, service_group_id,
                            s_pers=None,
                            c_pers=None,
                            status=1):
    def create(self, name, ip_address, protocol, port, service_group_id,
               s_pers=None, c_pers=None, status=1):  # WRONG WRONG WRONG

        params = {
            "virtual_server": {
                "name": name,
                "address": ip_address,
                "status": todo,
            },
            "vport_list": [
                {
                    extra_goo_from_def_struct: todo,
                    "service_group": service_group_id,
                    "port": port_todo, ##what is this?  enum?
                    "name": name + "_VPORT"
                }
            ]
       }
        # if protocol == "HTTP":
        #     vport_obj = request_struct_v2.vport_HTTP_obj.ds.toDict()
        # elif protocol == "HTTPS":
        #     vport_obj = request_struct_v2.vport_HTTPS_obj.ds.toDict()
        # else:
        #     vport_obj = request_struct_v2.vport_TCP_obj.ds.toDict()
        # if s_pers is not None:
        #     vport_obj['source_ip_persistence_template'] = s_pers
        # if c_pers is not None:
        #     vport_obj['cookie_persistence_template'] = c_pers
        # if self.device_info['autosnat']:
        #     vport_obj['source_nat_auto'] = 1

        self.http.post(self.url("slb.virtual_service.create"), params)

    def virtual_port_update(self, name, protocol, service_group_id,
                            s_pers=None,
                            c_pers=None,
                            status=1):
        vport_name = name + "_VPORT"
        if protocol is "HTTP":
            vport_update_req = (request_struct_v2.vport_HTTP_obj.call.update
                                .toDict().items())
        elif protocol is "HTTPS":
            vport_update_req = (request_struct_v2.vport_HTTPS_obj.call.update
                                .toDict().items())
        else:
            vport_update_req = (request_struct_v2.vport_TCP_obj.call.update
                                .toDict().items())

        # First, grab the current port config
        vport_res = self.virtual_port_get(vport_name, protocol)
        if 'virtual_service' not in vport_res:
            raise a10_ex.SearchError(term="vPort Object %s" % name)

        # Now apply the changes
        if s_pers is not None:
            vport_res['source_ip_persistence_template'] = s_pers
        elif c_pers is not None:
            vport_res['cookie_persistence_template'] = c_pers

        vport_res['service_group'] = service_group_id
        vport_res['status'] = status

        # Write the changes to the port
        r = self.send(tenant_id=self.tenant_id,
                      method=vport_update_req[0][0],
                      url=vport_update_req[0][1],
                      body=vport_res)

        if self.inspect_response(r) is not True:
            raise a10_ex.VipUpdateError(vip=name)

    def delete(self, name):
        self.http.post(self.url("slb.virtual_service.delete"),
                       {"name": name})


vport_HTTP_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.delete&session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&method=slb."
                               "virtual_service.getAll&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.search&session_id=%s"},
             "deleteall": {
                 "POST": "/services/rest/v2.1/?format=json&method=slb."
                         "virtual_service.deleteAll&session_id=%s"},
             "fetchstatistics": {
             "POST": "/services/rest/v2.1/?format=json&method=slb."
                     "virtual_service.fetchStatistics&session_id=%s"},
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&method=slb."
                        "virtual_service.fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "protocol": 11,
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "send_reset": 0,
        "port": 80,
        "service_group": "",
        "vport_acl_id": 0,
        "auto_source_nat": 0,
        "extended_stats": 0,
        "server_ssl_template": "",
        "aflex_list": [],
        "status": 1,
        "default_selection": 1,
        "http_template": "",
        "source_nat": "",
        "cookie_persistence_template": "",
        "conn_reuse_template": "",
        "name": "",
        "tcp_proxy_template": "",
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "ram_cache_template": "",
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []
    }
}))

vport_HTTPS_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.delete&session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&method=slb."
                               "virtual_service.getAll&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.search&session_id=%s"},
             "deleteall": {
                 "POST": "/services/rest/v2.1/?format=json&method=slb."
                         "virtual_service.deleteAll&session_id=%s"},
             "fetchstatistics": {
             "POST": "/services/rest/v2.1/?format=json&method=slb."
                     "virtual_service.fetchStatistics&session_id=%s"},
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&method=slb."
                        "virtual_service.fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "protocol": 12,
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "send_reset": 0,
        "port": 443,
        "service_group": "",
        "auto_source_nat": 0,
        "vport_acl_id": 0,
        "extended_stats": 0,
        "server_ssl_template": "",
        "aflex_list": [],
        "status": 1,
        "client_ssl_template": "",
        "source_ip_persistence_template": "",
        "default_selection": 1,
        "http_template": "",
        "source_nat": "",
        "conn_reuse_template": "",
        "name": "",
        "tcp_proxy_template": "",
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "ram_cache_template": "",
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []
    }
}))

vport_TCP_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.delete&session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&method=slb."
                               "virtual_service.getAll&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "virtual_service.search&session_id=%s"},
             "deleteall": {
                 "POST": "/services/rest/v2.1/?format=json&method=slb."
                         "virtual_service.deleteAll&session_id=%s"},
             "fetchstatistics": {
             "POST": "/services/rest/v2.1/?format=json&method=slb."
                     "virtual_service.fetchStatistics&session_id=%s"},
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&method=slb."
                        "virtual_service.fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "protocol": 2,
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "tcp_template": "",
        "send_reset": 0,
        "port": '',
        "service_group": "",
        "vport_acl_id": 0,
        "extended_stats": 0,
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&method=slb."
                        "virtual_service.fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "protocol": 2,
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "tcp_template": "",
        "send_reset": 0,
        "port": '',
        "service_group": "",
        "vport_acl_id": 0,
        "extended_stats": 0,
        "aflex_list": [],
        "status": 1,
        "auto_source_nat": 0,
        "direct_server_return": 0,
        "source_ip_persistence_template": "",
        "default_selection": 1,
        "source_nat": "",
        "name": "",
        "ha_connection_mirror": 0,
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []
    }
}))


