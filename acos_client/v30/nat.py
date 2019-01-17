# Copyright 2015, A10 Networks
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

from acos_client import errors as acos_errors
from acos_client.v30 import base


class Nat(base.BaseV30):
    @property
    def pool(self):
        return self.Pool(self.client)

    class Pool(base.BaseV30):
        url_prefix = "/ip/nat/pool/"

        def _set(self, name, start_ip, end_ip, mask, ip_rr=None, vrid=None, **kwargs):
            params = {
                "pool": self.minimal_dict(
                    {
                        'pool-name': name,
                        'start-address': start_ip,
                        'end-address': end_ip,
                        'netmask': mask,
                    }
                ),
            }

            if ip_rr:
                params["pool"]["ip-rr"] = ip_rr

            if vrid:
                params["pool"]["vrid"] = vrid

            if self.exists(name):
                self._post(self.url_prefix + name, params, **kwargs)
            else:
                self._post(self.url_prefix, params, **kwargs)

        def get(self, name):
            return self._get(self.url_prefix + name)

        def exists(self, name):
            try:
                self.get(name)
                return True
            except acos_errors.NotFound:
                return False

        def all(self):
            return self._get(self.url_prefix)

        def create(self, name, start_ip, end_ip, mask, ip_rr, vrid, **kwargs):
            if self.exists(name):
                raise acos_errors.Exists

            self._set(name, start_ip, end_ip, mask, ip_rr, vrid, **kwargs)

        def delete(self, name, **kwargs):
            self._delete(self.url_prefix + name)

        def stats(self, name='', **kwargs):
            return self._get(self.url_prefix + name + '/stats', **kwargs)

        def all_stats(self, **kwargs):
            return self.stats()
