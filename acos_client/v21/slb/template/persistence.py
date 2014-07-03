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


class CookiePersistence(base.BaseV21):

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


class SourceIpPersistence(base.BaseV21):

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

COOKIE_PER_TEMP_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "template.cookie_persistence."
                                "create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "delete&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "search&session_id=%s"}
             },
    "ds": {
        "cookie_persistence_template": {
            "name": "",
            "expire_exist": 0,
            "expire": 3600,
            "cookie_name": "",
            "domain": "",
            "path": "",
            "match_type": 0,
            "match_all": 0,
            "insert_always": 0,
            "dont_honor_conn": 0
        }
    }
}))




SOURCE_IP_TEMP_OBJ = wrapper(copy.deepcopy({
    "call": {
        "create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                           "template.src_ip_persistence"
                           ".create&session_id=%s"},
        "update": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                           "template.src_ip_persistence.update&session_id=%s"},
        "delete": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                           "template.src_ip_persistence.delete&session_id=%s"},
        "search": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                           "template.src_ip_persistence.search&session_id=%s"}
    },
    "ds": {
        "src_ip_persistence_template": {
            "name": "src_ip",
            "match_type": 1,
            "match_all": 0,
            "timeout": 1800,
            "no_honor_conn": 0,
            "incl_sport": 0,
            "include_dstip": 0,
            "hash_persist": 0,
            "enforce_high_priority": 0,
            "netmask": "255.255.255.255",
            "netmask6": 96
        }
    }
}))

    def persistence_exists(self, persist_type, name):
        if persist_type == 'SOURCE_IP':
            req = (request_struct_v2.SOURCE_IP_TEMP_OBJ.call.search
                   .toDict().items())
        elif persist_type == 'HTTP_COOKIE':
            req = (request_struct_v2.COOKIE_PER_TEMP_OBJ.call.search
                   .toDict().items())
        else:
            raise a10_ex.TemplateCreateError(template=name)

        r = self.send(tenant_id=self.tenant_id,
                      method=req[0][0],
                      url=req[0][1],
                      body={"name": name})
        return self.inspect_response(r)

    def persistence_create(self, persist_type, name):
        if persist_type == 'SOURCE_IP':
            args = request_struct_v2.SOURCE_IP_TEMP_OBJ.ds.toDict()
            args["src_ip_persistence_template"]['name'] = name
            req = (request_struct_v2.SOURCE_IP_TEMP_OBJ.call
                   .create.toDict().items())
        elif persist_type == 'HTTP_COOKIE':
            args = request_struct_v2.COOKIE_PER_TEMP_OBJ.ds.toDict()
            args["cookie_persistence_template"]['name'] = name
            req = (request_struct_v2.COOKIE_PER_TEMP_OBJ
                   .call.create.toDict().items())
        else:
            raise a10_ex.TemplateCreateError(template=name)

        r = self.send(tenant_id=self.tenant_id,
                      method=req[0][0],
                      url=req[0][1],
                      body=args)

        if self.inspect_response(r) is not True:
            raise a10_ex.TemplateCreateError(template=name)

    def persistence_delete(self, persist_type, name):
        if persist_type == "SOURCE_IP":
            delete_per_temp = (request_struct_v2
                               .SOURCE_IP_TEMP_OBJ.call.delete
                               .toDict().items())
        elif persist_type == 'HTTP_COOKIE':
            delete_per_temp = (request_struct_v2
                               .COOKIE_PER_TEMP_OBJ.call.delete
                               .toDict().items())
        else:
            LOG.debug("Unknown persistence type passed to delete: %s",
                      persist_type)
            return None

        r = self.send(tenant_id=self.tenant_id,
                      method=delete_per_temp[0][0],
                      url=delete_per_temp[0][1],
                      body={'name': name})
        if self.inspect_response(r) is not True:
            LOG.debug("Tempalte %s will be orphaned", name)
