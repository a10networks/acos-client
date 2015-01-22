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


class Port(base.BaseV21):

    # Protocols
    TCP = 2
    UDP = 3

    def _set(self, action, name, port_num, protocol, **kwargs):

        params = {
            "name": name,
            "port": {
                "port_num": port_num,
                "protocol": protocol,
            }
        }

        return self._post(action, params, **kwargs)

    def create(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.create", name, port_num, protocol,
                         **kwargs)

    def update(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.update", name, port_num, protocol,
                         **kwargs)

    def all_update(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.updateAll", name, port_num, protocol,
                         **kwargs)

    def delete(self, name, port_num, protocol, **kwargs):
        self._set("slb.server.port.delete", name, port_num, protocol, **kwargs)

    def all_delete(self, name, **kwargs):
        self._get("slb.server.port.deleteAll",  {"name": name}, **kwargs)
