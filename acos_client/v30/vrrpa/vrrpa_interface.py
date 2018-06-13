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
from acos_client.v30.vrrp.blade_params import BladeParameters


class VirtualRouterRP(base.BaseV30):

    def __init__(self, client):
        super(Interface, self).__init__(client)
        self.base_url="/axapi/v3/vrrp-a/vrid/"

    @property
    def blade(self, vrid_val):
        self.get(vrid_val) # ensure that vrid exists
        return BladeParemeters(vrid_val)

    def get(self, vrid_val):
        return self._get 


    def create(self, vrid_val, blade_params=None):
        self.

    def update(self, vrid_val, blade_params=None):
        pass

    def delete(self, vrid_val):
        return self._delete(self.base_url + str(vrid_val))
