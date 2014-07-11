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


class VirtualService(base.BaseV21):   # aka VirtualPort

    # Protocols
    TCP = 2
    UDP = 3
    HTTP = 11
    HTTPS = 12

    def get(self, name):
        return self.http.post(self.url("slb.virtual_service.search"),
                              {'name': name})

    def _set(self, action, service_group_name, name, protocol=None, port=None,
             s_pers_name=None, c_pers_name=None, status=1):
        params = {
            "virtual_service": self.minimal_dict({
                "name": name,
                "service_group": service_group_name,
                "protocol": protocol,
                "port": port,
                "source_ip_persistence_template": s_pers_name,
                "cookie_persistence_template": c_pers_name,
                "status": status
            })
        }

        self.http.post(self.url(action), params)

    def create(self, *args):
        self._set('slb.virtual_service.create', *args)

    def update(self, *args):
        self._set('slb.virtual_service.update', *args)

    def delete(self, name):
        self.http.post(self.url("slb.virtual_service.delete"), {"name": name})
