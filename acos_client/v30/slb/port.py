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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client.v30 import base


class Port(base.BaseV30):

    url_base_tmpl = "/slb/server/{server}/port/"
    url_port_tmpl = "{port}+{protocol}/"

    def create(self, server_name, port, protocol, **kwargs):
        return self._set(server_name, port, protocol, **kwargs)

    def update(self, server_name, port, protocol, **kwargs):
        return self._set(server_name, port, protocol, update=True, **kwargs)

    def delete(self, server_name, port, protocol, **kwargs):
        url = (self.url_base_tmpl + self.url_port_tmpl).format(server=server_name,
                                                               port=port,
                                                               protocol=protocol)

        return self._delete(url)

    def _set(self, server_name, port, protocol, update=False, **kwargs):
        url = self.url_base_tmpl.format(server=server_name)

        params = {
            "port": {
                "conn-resume": kwargs.get("conn_resume", None),
                "conn-limit": kwargs.get("conn_limit"),
                "stats-data-action": kwargs.get("stats_data_action", "stats-data-enable"),
                "weight": kwargs.get("weight", 1),
                "port-number": port,
                "range": kwargs.get("range", 0),
                "action": kwargs.get("action", "enable"),
                "protocol": protocol
            }
        }

        if update:
            url += self.url_port_tmpl.format(port=port, protocol=protocol)

            return self._put(url, params, **kwargs)
        else:
            return self._post(url, params, **kwargs)
