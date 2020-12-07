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

    def create(self, server_name, port, protocol, max_retries=None, timeout=None,
               conn_resume=None, conn_limit=None, stats_data_action="stats-data-enable",
               weight=1, range=0, action="enable", **kwargs):
        url = self.url_base_tmpl.format(server=server_name)
        params = self._set(server_name, port, protocol, conn_resume=conn_resume, conn_limit=conn_limit,
                           stats_data_action=stats_data_action, weight=weight, range=range, action=action)
        return self._post(url, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def update(self, server_name, port, protocol, max_retries=None, timeout=None,
               conn_resume=None, conn_limit=None, stats_data_action="stats-data-enable",
               weight=1, range=0, action="enable", **kwargs):
        url = self.url_base_tmpl.format(server=server_name)
        url += self.url_port_tmpl.format(port=port, protocol=protocol)
        params = self._set(server_name, port, protocol, conn_resume=conn_resume, conn_limit=conn_limit,
                           stats_data_action=stats_data_action, weight=weight, range=range, action=action)
        return self._put(url, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def delete(self, server_name, port, protocol, **kwargs):
        url = (self.url_base_tmpl + self.url_port_tmpl).format(server=server_name,
                                                               port=port,
                                                               protocol=protocol)

        return self._delete(url)

    def _set(self, server_name, port, protocol, conn_resume=None, conn_limit=None,
             stats_data_action="stats-data-enable", weight=1, range=0, action="enable"):
        params = {
            "port": {
                "stats-data-action": stats_data_action,
                "weight": weight,
                "port-number": port,
                "range": range,
                "action": action,
                "protocol": protocol
            }
        }

        if conn_resume:
            params['port']['conn-resume'] = conn_resume

        if conn_limit:
            params['port']['conn-limit'] = conn_limit

        return params
