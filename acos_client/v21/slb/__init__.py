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

import acos_client.v21.base as base

from aflex import Aflex
from class_list import ClassList
from hm import HealthMonitor
from server import Server
from service_group import ServiceGroup
from template import Template
from virtual_server import VirtualServer
from virtual_service import VirtualService


class SLB(base.BaseV21):
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
    def aflex(self):
        return Aflex(self.client)

    @property
    def class_list(self):
        return ClassList(self.client)

    @property
    def virtual_service(self):
        return VirtualService(self.client)

    @property
    def common(self):
        raise NotImplementedError("slb.common support is not available using AXAPI v2.1")
