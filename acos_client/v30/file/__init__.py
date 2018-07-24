# Copyright 2015,  Tobit Raff,  A10 Networks.
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

from acos_client.v30.file.ssl_cert import SSLCert
from acos_client.v30.file.ssl_key import SSLKey


class File(base.BaseV30):
    @property
    def ssl_cert(self):
        return SSLCert(self.client)

    @property
    def ssl_key(self):
        return SSLKey(self.client)
