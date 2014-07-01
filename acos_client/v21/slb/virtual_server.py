
virtual_server_object = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method="
                                "slb.virtual_server.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.virtual_server.update&"
                                "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.virtual_server.delete&"
                                "session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&"
                               "method=slb.virtual_server.getAll&"
                               "session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.virtual_server.search&"
                                "session_id=%s"},
             "deleteall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.virtual_server."
                                   "deleteAll&session_id=%s"},
             "fetchstatistics": {
             "POST": "/services/rest/v2.1/?format=json&method=slb."
                     "virtual_server.fetchStatistics&session_id=%s"},
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&method=slb."
                        "virtual_server.fetchAllStatistics&"
                        "session_id=%s"}
             },
    "ds": {"virtual_server": {
        "status": 1,
        "disable_vserver_on_condition": 0,
        "name": "foa",
        "vip_template": "default",
        "pbslb_template": "",
        "redistribution_flagged": 0,
        "extended_stats": 0,
        "ha_group": {
            "status": 0,
            "ha_group_id": 0,
            "dynamic_server_weight": 0
        },
        "arp_status": 1,
        "address": "192.168.212.121",
        "vport_list": [

        ],
        "stats_data": 1
    }
    }
}))

    def virtual_server_get(self, name):
        service_group_search_req = (request_struct_v2.service_group_json_obj
                                    .call.search.toDict().items())

        r = self.send(tenant_id=self.tenant_id,
                      method=service_group_search_req[0][0],
                      url=service_group_search_req[0][1],
                      body={'name': name})
        return r

    def virtual_server_create(self, name, ip_address, protocol, port,
                              service_group_id,
                              s_pers=None,
                              c_pers=None,
                              status=1):

        create_vip_req = (request_struct_v2.virtual_server_object.call
                          .create.toDict().items())

        vs = request_struct_v2.virtual_server_object.ds.toDict()

        vs['virtual_server']['address'] = ip_address
        vs['virtual_server']['name'] = name
        vs['virtual_server']['status'] = status

        if protocol == "HTTP":
            vport_obj = request_struct_v2.vport_HTTP_obj.ds.toDict()
        elif protocol == "HTTPS":
            vport_obj = request_struct_v2.vport_HTTPS_obj.ds.toDict()
        else:
            vport_obj = request_struct_v2.vport_TCP_obj.ds.toDict()

        vport_obj['service_group'] = service_group_id
        vport_obj['port'] = port
        vport_obj['name'] = name + "_VPORT"

        if s_pers is not None:
            vport_obj['source_ip_persistence_template'] = s_pers
        else:
            vport_obj['source_ip_persistence_template'] = ""

        if c_pers is not None:
            vport_obj['cookie_persistence_template'] = c_pers
        else:
            vport_obj['cookie_persistence_template'] = ""

        if self.device_info['autosnat']:
            vport_obj['source_nat_auto'] = 1
        vs['vport_list'] = [vport_obj]

        r = self.send(tenant_id=self.tenant_id,
                      method=create_vip_req[0][0],
                      url=create_vip_req[0][1],
                      body=vs)

        if self.inspect_response(r) is not True:
            raise a10_ex.VipCreateError(vip=name)


    def virtual_server_delete(self, name):
        vs_delete_req = (request_struct_v2.virtual_server_object.call.
                         delete.toDict().items())

        r = self.send(tenant_id=self.tenant_id,
                      method=vs_delete_req[0][0],
                      url=vs_delete_req[0][1],
                      body={'name': name})
        if self.inspect_response(r) is not True:
            raise a10_ex.VipDeleteError(vip=name)


    def stats(self, name):
        stats_req = (request_struct_v2.virtual_server_object.call
                     .fetchstatistics
                     .toDict().items().items())

        return self.send(tenant_id=self.tenant_id,
                         method=stats_req[0][0],
                         url=stats_req[0][1],
                         body={"name": name})



