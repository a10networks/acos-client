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

        def _set(self, name, start_ip, end_ip, mask, ip_rr=None, vrid=None, gateway=None):
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

            if gateway:
                params["pool"]['gateway'] = gateway

            return params

        def get(self, name):
            return self._get(self.url_prefix + name)

        def try_get(self, name):
            try:
                return self.get(name)
            except acos_errors.NotFound:
                return None

        def exists(self, name):
            try:
                self.get(name)
                return True
            except acos_errors.NotFound:
                return False

        def all(self):
            return self._get(self.url_prefix)

        def create(self, pool_name, start_address, end_address, netmask, ip_rr=None, vrid=None,
                   gateway=None, max_retries=None, timeout=None, **kwargs):
            if self.exists(pool_name):
                raise acos_errors.Exists
            params = self._set(pool_name, start_address, end_address, netmask,
                               ip_rr=ip_rr, vrid=vrid, gateway=gateway)
            axapi_args = {'pool': kwargs}
            return self._post(self.url_prefix, params, max_retries=max_retries,
                              timeout=timeout, axapi_args=axapi_args)

        def delete(self, name, **kwargs):
            self._delete(self.url_prefix + name)

        def stats(self, name='', max_retries=None, timeout=None, **kwargs):
            return self._get(self.url_prefix + name + '/stats',
                             max_retries=max_retries, timeout=timeout,
                             **kwargs)

        def all_stats(self, **kwargs):
            return self.stats()
