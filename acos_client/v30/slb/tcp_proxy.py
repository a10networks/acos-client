# Copyright 2019,  Omkar Telee,  A10 Networks.
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


class TcpProxy(base.BaseV30):

    # Proxy Protocol Version
    PROXY = "v1"
    PROXYV2 = "v2"

    url_prefix = '/slb/template/tcp-proxy/'

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def exists(self, name, **kwargs):
        try:
            self.get(name, **kwargs)
            return True
        except acos_errors.NotFound:
            return False

    def _set(self, name, version, **kwargs):

        params = {
            "tcp-proxy":{
                "name": name,
                "proxy-header": {
                    "proxy-header-action": "insert",
                    "version": version
                }
            }
        }

        response = self._post(self.url_prefix, params, **kwargs)
        return response

    def create(self, name, version, **kwargs):
        return self._set(name, version, **kwargs)

    def update(self, name, version, **kwargs):
        return self._set(name, version, **kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)
