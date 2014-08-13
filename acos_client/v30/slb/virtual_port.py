# Copyright 2014,  Jeff Buttars,  A10 Networks.
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

import json
import acos_client.v30.base as base


class VirtualPort(base.BaseV30):

    # Protocols
    TCP = 2
    UDP = 3
    HTTP = 11
    HTTPS = 12
    url_tmpl = '/slb/virtual-server/{name}/port/{port_number}+{protocol}'

    def _set(self, virtual_server_name, name, protocol, port,
             service_group_name,
             s_pers_name=None, c_pers_name=None, status=1):

        url = self.url_tmpl.format(
            name=virtual_server_name,
            port_number=port,
            protocol=protocol
        )

        params = {
            "vport": self.minimal_dict({
                "name": name,
                "service_group": service_group_name,
                "protocol": protocol,
                "port": int(port),
                "source_ip_persistence_template": s_pers_name,
                "cookie_persistence_template": c_pers_name,
                "status": status
            })
        }
        return self.http.post(self.url(url), json.dumps(params))

    def create(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1):
        return self._set(virtual_server_name,
                         name, protocol, port, service_group_name,
                         s_pers_name, c_pers_name, status)

    def update(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1):
        return self._set(virtual_server_name,
                         name, protocol, port, service_group_name,
                         s_pers_name, c_pers_name, status)

    def delete(self, virtual_server_name, name, protocol, port):

        url = self.url_tmpl.format(
            name=virtual_server_name,
            port_number=port,
            protocol=protocol
        )
        params = {
            "vport": {
                "name": name,
                "protocol": protocol,
                "port": int(port)
            }
        }

        return self.http.delete(self.url(url), json.dumps(params))
