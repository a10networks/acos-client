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

import acos_client
import acos_client.axapi_http as axapi_http
import acos_client.errors as acos_errors

from v21.session import Session
from v21.slb import SLB
from v21.system import System


class Client(object):

    def __init__(self, host, version, username, password, port=None,
                 protocol=None):
        if self._just_digits(version) != acos_client.AXAPI_21:
            raise acos_errors.ACOSUnsupportedVersion()
        self.http = axapi_http.HttpClient(host, port, protocol)
        self.session = Session(self, username, password)
        self.current_partition = 'shared'

    def _just_digits(self, s):
        return ''.join(i for i in s if i.isdigit())

    @property
    def system(self):
        return System(self)

    @property
    def slb(self):
        return SLB(self)