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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client.v30 import base
from acos_client.v30.slb.port import Port


class Server(base.BaseV30):

    url_prefix = '/slb/server/'

    def get(self, name, max_retries=None, timeout=None, **kwargs):
        return self._get(self.url_prefix + name, max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)

    def _set(self, name, ip_address, status=1, server_templates=None, port_list=None,
             conn_resume=None, conn_limit=None, health_check=None, **kwargs):
        params = {
            "server": {
                "name": name,
                "action": 'enable' if status else 'disable',
                "conn-resume": conn_resume,
                "conn-limit": conn_limit,
                "health-check": health_check,
            }
        }

        if port_list:
            params['server']['port-list'] = port_list

        if self._is_ipv6(ip_address):
            params['server']['server-ipv6-addr'] = ip_address
        else:
            params['server']['host'] = ip_address

        if server_templates:
            server_templates = {k: v for k, v in server_templates.items() if v}
            params['server']['template-server'] = server_templates.get('template-server')

        return params

    def create(self, name, ip_address, status=1, server_templates=None,
               port_list=None, max_retries=None, timeout=None,
               conn_resume=None, conn_limit=None, health_check=None, **kwargs):
        params = self._set(name, ip_address, status=status, port_list=port_list,
                           conn_resume=conn_resume, conn_limit=conn_limit, health_check=health_check,
                           server_templates=server_templates, **kwargs)
        return self._post(self.url_prefix, params, max_retries=max_retries, timeout=timeout,
                          axapi_args=kwargs)

    def update(self, name, ip_address, status=1, server_templates=None,
               port_list=None, max_retries=None, timeout=None,
               conn_resume=None, conn_limit=None, health_check=None, **kwargs):
        params = self._set(name, ip_address, status=status, port_list=port_list,
                           conn_resume=conn_resume, conn_limit=conn_limit, health_check=health_check,
                           server_templates=server_templates, **kwargs)
        return self._post(self.url_prefix + name, params, max_retries=max_retries, timeout=timeout,
                          axapi_args=kwargs)

    def replace(self, name, ip_address, status=1, server_templates=None,
                port_list=None, max_retries=None, timeout=None,
                conn_resume=None, conn_limit=None, health_check=None, **kwargs):
        params = self._set(name, ip_address, status=status, port_list=port_list,
                           conn_resume=conn_resume, conn_limit=conn_limit, health_check=health_check,
                           server_templates=server_templates, **kwargs)
        return self._put(self.url_prefix + name, params, max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)

    @property
    def port(self):
        return Port(self.client)
