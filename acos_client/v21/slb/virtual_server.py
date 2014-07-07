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

import acos_client.v21.base as base


class VirtualServer(base.BaseV21):

    def get(self, name):
        return self.http.post(self.url("slb.virtual_server.search"),
                              {'name': name})

    def create(self, name, ip_address, protocol, port, service_group_id,
               s_pers=None, c_pers=None, status=1):
        params = {
            "virtual_server": {
                "name": name,
                "address": ip_address,
                "status": status,
            },
            "vport_list": [
                {
                    "name": name + "_VPORT",
                    "protocol": protocol,
                    "port": port,
                    "service_group": service_group_id,
                    "status": status
                }
            ]
        }
        if s_pers is not None:
            params['vport_list'][0]['source_ip_persistence_template'] = s_pers
        elif c_pers is not None:
            params['vport_list'][0]['cookie_persistence_template'] = c_pers

        self.http.post(self.url("slb.virtual_server.create"), params)

    def delete(self, name):
        self.http.post(self.url("slb.virtual_server.delete"),
                       {"name": name})

    def stats(self, name):
        return self.http.post(self.url("slb.virtual_server.fetchStatistics"),
                              {"name": name})
