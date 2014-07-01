

server_json_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "server.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.server.update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.server.delete&session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&"
                               "method=slb.server.getAll&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.server.search&session_id=%s"},
             "deleteall": {"POST": "/services/rest/v2.1/?"
                                   "format=json&method=slb.server."
                                   "deleteAll&session_id=%s"},
             "fetchstatistics": {
                 "POST": "/services/rest/v2.1/?format=json&method=slb."
                         "server.fetchStatistics&session_id=%s"},
             "fetchallstatistics": {"GET": "/services/rest/v2.1/"
                                           "?format=json&method=slb."
                                           "server."
                                           "fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "server": {
            "name": "",
            "host": "",
            "gslb_external_address": "0.0.0.0",
            "weight": '',
            "health_monitor": "(default)",
            "status": 1,
            "conn_limit": '',
            "conn_limit_log": 1,
            "conn_resume": 0,
            "stats_data": 1,
            "extended_stats": 0,
            "slow_start": 0,
            "spoofing_cache": 0,
            "template": "default",
            "port_list": [

            ]
        }
    }
}))



    def server_get(self, server_name):
        server_search_req = (request_struct_v2.server_json_obj.call.search
                             .toDict().items())

        return self.send(tenant_id=self.tenant_id,
                         method=server_search_req[0][0],
                         url=server_search_req[0][1],
                         body={'name': server_name})

    def server_create(self, server_name, ip_address):
        server_create_req = (request_struct_v2.server_json_obj.call.create
                             .toDict().items())
        server_ds = (request_struct_v2.server_json_obj.ds.toDict())
        server_ds['server']['name'] = server_name
        server_ds['server']['host'] = ip_address

        r = self.send(tenant_id=self.tenant_id,
                      method=server_create_req[0][0],
                      url=server_create_req[0][1],
                      body=server_ds)

        if self.inspect_response(r) is not True:
            raise a10_ex.MemberCreateError(member=server_name)

    def server_delete(self, server_name):
        server_delete_req = (request_struct_v2.server_json_obj.call.delete
                             .toDict().items())
        server_ds = {"server": {"name": server_name}}

        r = self.send(tenant_id=self.tenant_id,
                      method=server_delete_req[0][0],
                      url=server_delete_req[0][1],
                      body=server_ds)

        if self.inspect_response(r) is not True:
            raise a10_ex.MemberDeleteError(member=server_name)
