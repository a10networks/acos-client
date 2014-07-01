

server_port_list_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?"
                                "format=json&method=slb.server.port."
                                "create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?"
                                "format=json&method=slb.server.port."
                                "update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.server.port.delete&"
                                "session_id=%s"},
             "deleteall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.server.port."
                                   "deleteAll&session_id=%s"},
             "updateall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.server.port."
                                   "updateAll&session_id=%s"}

             },
    "ds": {
        "port_num": '1-65535',
        "protocol": {'TCP': 2, 'UDP': 3},
        "status": 1,
        "weight": 1,
        "no_ssl": 0,
        "conn_limit": 8000000,
        "conn_limit_log": 1,
        "conn_resume": 0,
        "template": "default",
        "stats_data": 1,
        "health_monitor": "(default)",
        "extended_stats": 0
    }
}))


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



    def virtual_port_get(self, name, protocol):
        vport_name = name + "_VPORT"
        if protocol is "HTTP":
            vport_obj_req = (request_struct_v2.vport_HTTP_obj.call.search
                             .toDict().items())
        elif protocol is "HTTPS":
            vport_obj_req = (request_struct_v2.vport_HTTPS_obj.call.search
                             .toDict().items())
        else:
            vport_obj_req = (request_struct_v2.vport_TCP_obj.call
                             .search.toDict().items())

        r = self.send(tenant_id=self.tenant_id,
                      method=vport_obj_req[0][0],
                      url=vport_obj_req[0][1],
                      body={"name": vport_name})
        return r


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

