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

import acos_client.errors as acos_errors
import acos_client.v30.base as base

from virtual_port import VirtualPort


class VirtualServer(base.BaseV30):
    url_prefix = '/slb/virtual-server/'

    @property
    def vport(self):
        return VirtualPort(self.client)

    def all(self):
        return self._get(self.url_prefix)

    def get(self, name):
        return self._get(self.url_prefix + name)

    def _set(self, name, ip_address=None, status='stats-data-enable',
             update=False, **kwargs):
        params = {
            "virtual-server": self.minimal_dict({
                "name": name,
                "ip-address": ip_address,
            }),
        }

        if not update:
            name = ''

        self._post(self.url_prefix + name, params, **kwargs)

    def create(self, name, ip_address, status='stats-data-enable', **kwargs):
        try:
            self.get(name)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists

        self._set(name, ip_address, status, **kwargs)

    def update(self, name, ip_address=None, status='stats-data-enable',
               **kwargs):
        self._set(name, ip_address, status, update=True, **kwargs)

    def delete(self, name):
        self._delete(self.url_prefix + name)

    def stats(self, name='', **kwargs):
        # resp = self._get(self.url_prefix + name + '/stats/')
        resp = self._get(self.url_prefix + name + '/stats', **kwargs)
        return resp
        # raise acos_errors.NotImplemented()
