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
from virtual_port import VirtualPort


class VirtualServer(base.BaseV30):
    url_prefix = '/slb/virtual-server/'

    @property
    def vport(self):
        return VirtualPort(self.client)

    def get(self, name):
        return self.http.get(self.url(self.url_prefix + name))

    def _set(self, name, ip_address=None, status=1):
        params = {
            "virtual_server": self.minimal_dict({
                "name": name,
                "address": ip_address,
                "status": status,
            }),
        }

        self.http.post(self.url(self.url_prefix + name), json.dumps(params))

    def create(self, name, ip_address, status=1):
        self._set(name, ip_address, status)

    def update(self, name, ip_address=None, status=1):
        self._set(name, ip_address, status)

    def delete(self, name):
        self.http.delete(self.url(self.url_prefix + name))

    def stats(self, name):
        return self.http.get(self.url(self.url_prefix + name + '/stats/'))
