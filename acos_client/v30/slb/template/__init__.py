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

import acos_client.v30.base as base

from acos_client.v30.slb.template.l7 import HTTPTemplate
from acos_client.v30.slb.template.persistence import CookiePersistence
from acos_client.v30.slb.template.persistence import SourceIpPersistence
from acos_client.v30.slb.template.ssl import ClientSSL
from acos_client.v30.slb.template.ssl import ServerSSL
from acos_client.v30.slb.template.ssl import SSLCipher


class Template(base.BaseV30):

    @property
    def client_ssl(self):
        return ClientSSL(self.client)

    @property
    def cipher_ssl(self):
        return SSLCipher(self.client)

    @property
    def cookie_persistence(self):
        return CookiePersistence(self.client)

    @property
    def src_ip_persistence(self):
        return SourceIpPersistence(self.client)

    @property
    def server_ssl(self):
        return ServerSSL(self.client)

    @property
    def http_template(self):
        return HTTPTemplate(self.client)
