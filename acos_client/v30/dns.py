# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

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


class DNS(base.BaseV30):
    url_prefix = "/ip/dns/"

    def _set_dns(self, precedence, addr):
        addr_spec = {}

        if ':' in addr:
            addr_spec['ip-v6-addr'] = addr
        else:
            addr_spec['ip-v4-addr'] = addr

        payload = {precedence: addr_spec}

        return self._post(self.url_prefix + precedence, payload)

    def _set_suffix(self, suffix):

        payload = {'suffix': {'domain-name': suffix}}

        return self._post(self.url_prefix + 'suffix', payload)

    def set(self, primary=None, secondary=None, suffix=None):
        if primary is not None:
            self._set_dns('primary', primary)

        if secondary is not None:
            self._set_dns('secondary', secondary)

        if suffix is not None:
            self._set_suffix(suffix)
