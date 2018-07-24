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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client.v21 import base


class BaseSSL(base.BaseV21):

    def get(self, name, **kwargs):
        return self._post(("slb.template.%s.search" % self.template_type),
                          {'name': name}, **kwargs)

    def _set(self, action, name, cert_name, key_name, **kwargs):
        params = {
            "%s_template" % self.template_type: {
                "cert_name": cert_name,
                "key_name": key_name,
                "name": name
            }
        }
        self._post(action, params, **kwargs)

    def create(self, name, cert_name, key_name, **kwargs):
        self._set(("slb.template.%s.create" % self.template_type),
                  name, cert_name, key_name, **kwargs)

    def update(self, name, cert_name, key_name, **kwargs):
        self._set(("slb.template.%s.update" % self.template_type),
                  name, cert_name, key_name, **kwargs)

    def delete(self, name, **kwargs):
        self._post(("slb.template.%s.delete" % self.template_type),
                   {"name": name}, **kwargs)


class ClientSSL(BaseSSL):

    template_type = "client_ssl"


class ServerSSL(BaseSSL):

    template_type = "server_ssl"
