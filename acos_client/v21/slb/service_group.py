
service_group_json_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "service_group.create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.service_group.update&"
                                "session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.service_group.delete&"
                                "session_id=%s"},
             "getall": {"GET": "/services/rest/v2.1/?format=json&"
                               "method=slb.service_group.getAll&"
                               "session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json"
                                "&method=slb.service_group.search&"
                                "session_id=%s"},
             "deleteall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.service_group.deleteAll&"
                                   "session_id=%s"},
             "fetchstatistics": {
                 "POST": "/services/rest/v2.1/?format=json&method=slb."
                         "service_group.fetchStatistics&"
                         "session_id=%s"},
             "fetchallstatistics": {
                 "GET": "/services/rest/v2.1/?format=json&"
                        "method=slb.service_group."
                        "fetchAllStatistics&session_id=%s"}
             },
    "ds": {
        "service_group": {
            "name": "",
            "protocol": '',
            "lb_method": {'RoundRobin': 0,
                          'WeightedRoundRobin': 1,
                          'LeastConnection': 2,
                          'WeightedLeastConnection': 3,
                          'LeastConnectionOnServicePort': 4,
                          'WeightedLeastConnectionOnServicePort': 5,
                          'FastResponseTime': 6,
                          'LeastRequest': 7,

                          'StrictRoundRobin': 8,
                          'StateLessSourceIPHash': 9,
                          'StateLessSourceIPHashOnly': 10,
                          'StateLessDestinationIPHash': 11,
                          'StateLessSourceDestinationIPHash': 12,
                          'StateLessPerPackageRoundRobin': 13},
            "health_monitor": "",
            "min_active_member": {
                "status": 0,
                "number": 0,
                "priority_set": 0
            },
            "backup_server_event_log_enable": 0,
            "client_reset": 0,
            "stats_data": 1,
            "extended_stats": 0,
            "member_list": []
        }
    }
}))


   def service_group_get(self, name):
        pool_search_req = (request_struct_v2.service_group_json_obj.call
                           .search.toDict().items())

        return self.send(tenant_id=self.tenant_id,
                         method=pool_search_req[0][0],
                         url=pool_search_req[0][1],
                         body={'name': name})


    def service_group_create(self, name, lb_method='3'):
        pool_create_req = (request_struct_v2.service_group_json_obj.call
                           .create.toDict().items())

        pool_ds = (request_struct_v2.service_group_json_obj.ds.toDict())
        pool_ds['service_group']['protocol'] = "2"
        pool_ds['service_group']['name'] = name
        pool_ds['service_group']['lb_method'] = lb_method

        r = self.send(tenant_id=self.tenant_id,
                      method=pool_create_req[0][0],
                      url=pool_create_req[0][1],
                      body=pool_ds)

        if self.inspect_response(r) is not True:
            raise a10_ex.SgCreateError(sg=name)

    def service_group_update(self, name, lb_method='3'):
        pool_update_req = (request_struct_v2.service_group_json_obj.call
                           .update.toDict().items())

        r = self.service_group_get(name)
        r['service_group']['protocol'] = "2"
        r['service_group']['name'] = name
        r['service_group']['lb_method'] = lb_method

        r = self.send(tenant_id=self.tenant_id,
                      method=pool_update_req[0][0],
                      url=pool_update_req[0][1],
                      body=r)

        if self.inspect_response(r) is not True:
            raise a10_ex.SgUpdateError(sg=name)


    def service_group_update_hm(self, name, mon=""):
        pool_update_req = (request_struct_v2.service_group_json_obj.call
                           .update.toDict().items())
        args = {"service_group": {"name": name, "health_monitor": mon}}

        r = self.send(tenant_id=self.tenant_id,
                      method=pool_update_req[0][0],
                      url=pool_update_req[0][1],
                      body=args)

        if self.inspect_response(r, func='delete') is not True:
            raise a10_ex.SgUpdateError(sg=name)

    def service_group_delete(self, name):
        pool_delete_req = (request_struct_v2.service_group_json_obj.call
                           .delete.toDict().items())

        r = self.send(tenant_id=self.tenant_id,
                      method=pool_delete_req[0][0],
                      url=pool_delete_req[0][1],
                      body={'name': name})

        if self.inspect_response(r, func='delete') is not True:
            raise a10_ex.SgDeleteError(sg="sg delete failure")


