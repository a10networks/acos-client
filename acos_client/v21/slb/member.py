
'
service_group_member_obj = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method="
                                "slb.service_group.member.create&"
                                "session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.service_group.member."
                                "update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.service_group.member."
                                "delete&session_id=%s"},
             "deleteall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.service_group.member."
                                   "deleteAll&session_id=%s"},
             "updateall": {"POST": "/services/rest/v2.1/?format=json&"
                                   "method=slb.service_group.member."
                                   "updateAll&session_id=%s"}
             },
    "ds": {"name": "",
           "member": {"server": "", "port": "", "status": "1"}
           }
}))

    def member_create(self, name, server_name, port, status=1):
        member_create_req = (request_struct_v2.service_group_member_obj
                             .call.create.toDict().items())
        member_ds = (request_struct_v2.service_group_member_obj
                     .ds.toDict())

        member_ds['name'] = name
        member_ds['member']['server'] = server_name
        member_ds['member']['port'] = port
        member_ds['member']['status'] = status

        r = self.send(tenant_id=self.tenant_id,
                      method=member_create_req[0][0],
                      url=member_create_req[0][1],
                      body=member_ds)

        if self.inspect_response(r) is not True:
            raise a10_ex.MemberCreateError(member=server_name)


    def member_update(self, name, server_name, port, status=1):
        member_update_req = (request_struct_v2.service_group_member_obj
                             .call.update.toDict().items())
        member_ds = (request_struct_v2.service_group_member_obj
                     .ds.toDict())

        member_ds['name'] = name
        member_ds['member']['server'] = server_name
        member_ds['member']['port'] = port
        member_ds['member']['status'] = status

        r = self.send(tenant_id=self.tenant_id,
                      method=member_update_req[0][0],
                      url=member_update_req[0][1],
                      body=member_ds)

        if self.inspect_response(r) is not True:
            raise a10_ex.MemberUpdateError(member=server_name)

    def member_delete(self, name, server_name, server_port):
        member_delete_req = (request_struct_v2.service_group_member_obj
                             .call.delete.toDict().items())
        member_ds = {
            "name": name,
            "member": {
                "server": server_name,
                "port": server_port
            }
        }

        r = self.send(tenant_id=self.tenant_id,
                      method=member_delete_req[0][0],
                      url=member_delete_req[0][1],
                      body=member_ds)

        if self.inspect_response(r, func='delete') is not True:
            LOG.debug("response is %s", r)
            raise a10_ex.MemberDeleteError(member=name)
