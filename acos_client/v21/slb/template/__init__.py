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

from acos_client.v21.slb.template.persistence import CookiePersistence
from acos_client.v21.slb.template.persistence import SourceIpPersistence
from acos_client.v21.slb.template.template_ssl import ClientSSL
from acos_client.v21.slb.template.template_ssl import ServerSSL


class Template(base.BaseV21):

    @property
    def client_ssl(self):
        return ClientSSL(self.client)

    @property
    def server_ssl(self):
        return ServerSSL(self.client)

    @property
    def cookie_persistence(self):
        return CookiePersistence(self.client)

    @property
    def src_ip_persistence(self):
        return SourceIpPersistence(self.client)
