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

    # Protocols
    TCP = 2
    UDP = 3
    HTTP = 11
    HTTPS = 12

    def get(self, name):
        return self.http.post(self.url("slb.virtual_service.search"),
                              {'name': name + "_VPORT"})

    def update(self, name, protocol, service_group_id,
               s_pers=None, c_pers=None, status=1):
        params = self.get(name)

        if s_pers is not None:
            params['source_ip_persistence_template'] = s_pers
        elif c_pers is not None:
            params['cookie_persistence_template'] = c_pers

        params['service_group'] = service_group_id
        params['status'] = status

        self.http.post(self.url("slb.virtual_service.update"), params)


    def delete(self, name):
        self.http.post(self.url("slb.virtual_service.delete"),
                       {"name": name + "_VPORT"})
