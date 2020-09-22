# Copyright 2016, A10 Networks
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

from acos_client import errors as acos_errors
from acos_client.v30 import base
from acos_client.v30.vrrpa.blade_params import BladeParameters


class VRID(base.BaseV30):

    def __init__(self, client):
        super(VRID, self).__init__(client)
        self.client = client
        self.base_url = "/vrrp-a/vrid/"

    @property
    def blade(self):
        return BladeParameters(self.client)

    def get(self, vrid_val):
        return self._get(self.base_url + str(vrid_val))

    def exists(self, vrid_val):
        try:
            self.get(vrid_val)
            return True
        except acos_errors.NotFound:
            return False

    def _build_params(self, vrid_val, threshold=None, disable=None, floating_ips=[],
                      is_partition=False):
        vrid = {'vrid-val': vrid_val}
        vrid_floating_ips = None
        if floating_ips:
            if is_partition:
                ip_partition_list = [{'ip-address-partition': ip} for ip in floating_ips]
                vrid_floating_ips = {
                    'ip-address-part-cfg': ip_partition_list
                }
            else:
                ip_list = [{'ip-address': ip} for ip in floating_ips]
                vrid_floating_ips = {
                    'ip-address-cfg': ip_list
                }
            vrid['floating-ip'] = vrid_floating_ips

        if threshold or disable:
            threshold = threshold if threshold in range(0, 256) else 1
            disable = disable if disable in [0, 1] else 0
            preempt = {
                'threshold': threshold,
                'disable': disable
            }
            vrid['preempt-mode'] = preempt

        payload = {'vrid': vrid}
        return payload

    def create(self, vrid_val, threshold=None, disable=None, floating_ips=[], is_partition=False):
        return self._post(self.base_url, self._build_params(vrid_val, threshold, disable,
                                                            floating_ips, is_partition))

    def update(self, vrid_val, threshold=None, disable=None, floating_ips=[], is_partition=False):
        return self._put(self.base_url + str(vrid_val), self._build_params(vrid_val, threshold,
                                                                           disable, floating_ips,
                                                                           is_partition))

    def delete(self, vrid_val):
        return self._delete(self.base_url + str(vrid_val))
