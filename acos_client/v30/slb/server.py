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
from acos_client.v30.slb.port import Port


class Server(base.BaseV30):

    url_prefix = '/slb/server/'

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def create(self, name, ip_address, status=1, **kwargs):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
                "action": 'enable' if status else 'disable',
                "conn-resume": kwargs.get("conn_resume", None),
                "conn-limit": kwargs.get("conn_limit", 8000000),
            }
        }

        config_defaults = kwargs.get("config_defaults")

        if config_defaults:
            for k, v in six.iteritems(config_defaults):
                params['server'][k] = v

        # Two creates in a row apparently works in ACOS 4.0; stop that
        try:
            self.get(name, **kwargs)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists()

        return self._post(self.url_prefix, params, **kwargs)

    def update(self, name, ip_address, status=1, **kwargs):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
                "action": 'enable' if status else 'disable',
                "conn-resume": kwargs.get("conn_resume", None),
                "conn-limit": kwargs.get("conn_limit", 8000000),
            }
        }

        self.get(name, **kwargs)

        return self._post(self.url_prefix + name, params, **kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)

    @property
    def port(self):
        return Port(self.client)
