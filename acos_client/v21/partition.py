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


class Partition(base.BaseV21):

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

PARTITION_OBJ = wrapper(copy.deepcopy({
    "call": {
        "active": {"POST":
                   "/services/rest/v2.1/?format=json&method=system."
                   "partition.active&session_id=%s"},
        "create": {"POST": "/services/rest/v2.1/?format=json&method=system."
                           "partition.create&session_id=%s"},
        "update": {"POST": "/services/rest/v2.1/?format=json&method=system."
                           "partition.update&session_id=%s"},
        "delete": {"POST": "/services/rest/v2.1/?format=json&method=system."
                           "partition.delete&session_id=%s"},
        "search": {"POST": "/services/rest/v2.1/?format=json&method=system."
                           "partition.search&session_id=%s"}
    },
    "ds": {
        'partition': {
            'max_aflex_file': 32,
            'network_partition': 0,
            'name': ""}
    }
}))

    def partition_search(self, tenant_id=""):
        req_info = (request_struct_v2.PARTITION_OBJ.call.search.toDict()
                    .items())
        response = self.send(tenant_id=tenant_id, method=req_info[0][0],
                             url=req_info[0][1] % self.session_id,
                             body={"name": self.tenant_id[0:13]},
                             partition_ax=False,
                             close_session_after_request=False)
        if 'response' in response:
            if "err" in response['response']:
                if response['response']['err'] == 520749062:
                    return False
        elif "partition" in response:
            return True

    def partition_create(self, tenant_id=""):
        req_info = (request_struct_v2.PARTITION_OBJ.call.create.toDict()
                    .items())
        obj = request_struct_v2.PARTITION_OBJ.ds.toDict()
        obj['partition']['name'] = tenant_id[0:13]
        return self.send(tenant_id=tenant_id, method=req_info[0][0],
                         url=req_info[0][1] % self.session_id,
                         body=obj,
                         partition_ax=False,
                         close_session_after_request=False)

    def partition_delete(self, tenant_id=""):
        req_info = (request_struct_v2.PARTITION_OBJ.call.delete.toDict()
                    .items())
        self.close_session(tenant_id=self.tenant_id)
        self.get_session_id()
        r = self.send(tenant_id=tenant_id, method=req_info[0][0],
                      url=req_info[0][1] % self.session_id,
                      body={"name": self.tenant_id[0:13]},
                      partition_ax=False)
        if self.inspect_response(r) is not True:
            raise a10_ex.ParitionDeleteError(partition=tenant_id[0:13])

    def partition_active(self, tenant_id="", default=False):
        req_info = (request_struct_v2.PARTITION_OBJ.call.active.toDict()
                    .items())
        if default is True:
            name = "shared"
        else:
            name = tenant_id[0:13]
        return self.send(tenant_id=tenant_id, method=req_info[0][0],
                         url=req_info[0][1] % self.session_id,
                         body={"name": name},
                         partition_ax=False,
                         close_session_after_request=False)
