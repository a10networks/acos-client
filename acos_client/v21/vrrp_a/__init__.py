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

import acos_client.v21.base as base

from acos_client.v21.vrrp_a.failover import VRRPAFailoverPolicy
from acos_client.v21.vrrp_a.interface import VRRPAInterface
from acos_client.v21.vrrp_a.vrrp_global import VRRPAGlobal


class VRRPA(base.BaseV21):
    # For status args
    @property
    def vrrpa_global(self):
        return VRRPAGlobal(self.client)

    @property
    def interface(self):
        return VRRPAInterface(self.client)

    @property
    def failover_policy(self):
        return VRRPAFailoverPolicy(self.client)
