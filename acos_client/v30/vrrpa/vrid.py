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

from acos_client.v30 import base
from acos_client.v30.vrrpa.blade_params import BladeParameters

class VRID(base.BaseV30):

    def __init__(self, client):
        super(VRID, self).__init__(client)
        self.client = client
        self.base_url="/vrrp-a/vrid/"

    @property
    def blade(self):
        return BladeParameters(self.client) 

    def get(self, vrid_val):
        return self._get(self.base_url  + str(vrid_val))

    def create(self, vrid_val, threshold=None, disable=None):
        vrid = {'vrid-val': vrid_val}

        if threshold or disable:
            threshold = threshold if threshold else 1
            disable = disable if disable else 0
            preempt = {
                    'threshold': threshold,
                    'disable': disable
                }

            vrid['preempt-mode'] = preempt

        payload = {'vrid': vrid}
        self._post(self.base_url, payload)

    def update(self, vrid_val, threshold=None, disable=None):
        vrid = {'vrid-val': vrid_val}

        if threshold or disable:
            threshold = threshold if threshold else 1
            disable = disable if disable else 0
            preempt = {
                    'threshold': threshold,
                    'disable': disable
                }

            vrid['preempt-mode'] = preempt

        payload = {'vrid': vrid}
        self._put(self.base_url+str(vrid_val), payload)

    def delete(self, vrid_val):
        return self._delete(self.base_url + str(vrid_val))
