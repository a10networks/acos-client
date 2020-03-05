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
import six


from acos_client import errors as acos_errors
from acos_client.v30 import base


class Member(base.BaseV30):

    url_base_tmpl = '/slb/service-group/{gname}/member/'
    url_mbr_tmpl = '{name}+{port}/'

    STATUS_ENABLE = 0
    STATUS_DISABLE = 1

    def get(self, service_group_name, server_name, server_port, **kwargs):
        url = self.url_base_tmpl.format(gname=service_group_name)
        url += self.url_mbr_tmpl.format(
            name=server_name,
            port=server_port
        )

        return self._get(url, **kwargs)

    def get_oper(self, service_group_name, server_name, server_port, **kwargs):
        url = self.url_base_tmpl.format(gname=service_group_name)
        url += self.url_mbr_tmpl.format(
            name=server_name,
            port=server_port
        )
        return self._get(url + 'oper', **kwargs)

    def _write(self,
               service_group_name,
               server_name,
               server_port,
               status=STATUS_ENABLE,
               member_state=True,
               update=False, **kwargs):

        url = self.url_base_tmpl.format(gname=service_group_name)
        if update:
            url += self.url_mbr_tmpl.format(
                name=server_name,
                port=server_port
            )

        params = {
            "member": self.minimal_dict({
                "name": server_name,
                "port": int(server_port),
                # flip status code, becuase it's a disable flag in v30
                "member-stats-data-disable": status,
                "member-state": member_state and 'enable' or 'disable',
            })
        }

        config_defaults = kwargs.get("config_defaults")

        if config_defaults:
            for k, v in six.iteritems(config_defaults):
                params['member'][k] = v

        self._post(url, params, **kwargs)

    def create(self,
               service_group_name,
               server_name,
               server_port,
               status=STATUS_ENABLE,
               member_state=True, **kwargs):
        try:
            self.get(service_group_name, server_name, server_port)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists()

        self._write(service_group_name,
                    server_name, server_port, status, member_state, **kwargs)

    def update(self,
               service_group_name,
               server_name,
               server_port,
               status=STATUS_ENABLE,
               member_state=True, **kwargs):
        self._write(service_group_name,
                    server_name, server_port, status, member_state, update=True, **kwargs)

    def delete(self, service_group_name, server_name, server_port):
        url = self.url_base_tmpl.format(gname=service_group_name)
        url += self.url_mbr_tmpl.format(
            name=server_name,
            port=server_port
        )
        self._delete(url)
