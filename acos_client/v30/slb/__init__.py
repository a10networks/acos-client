# Copyright 2014-2016 A10 Networks.
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

import acos_client.v30.base as base

from acos_client.v30.slb.aflex_policy import AFlexPolicy
from acos_client.v30.slb.common import SLBCommon
from acos_client.v30.slb.hm import HealthMonitor
from acos_client.v30.slb.server import Server
from acos_client.v30.slb.service_group import ServiceGroup
from acos_client.v30.slb.template import Template
from acos_client.v30.slb.virtual_server import VirtualServer


class SLB(base.BaseV30):
    # For status args
    DOWN = 0
    UP = 1

    @property
    def hm(self):
        return HealthMonitor(self.client)

    @property
    def server(self):
        return Server(self.client)

    @property
    def service_group(self):
        return ServiceGroup(self.client)

    @property
    def template(self):
        return Template(self.client)

    @property
    def virtual_server(self):
        return VirtualServer(self.client)

    @property
    def aflex_policy(self):
        return AFlexPolicy(self.client)

    @property
    def common(self):
        return SLBCommon(self.client)

    def all(self):
        return self._get('/slb/')
