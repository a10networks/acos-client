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

from v21.session import Session as v21_Session
from v21.slb import SLB as v21_SLB
from v21.system import System as v21_System
from v30.session import Session as v30_Session
from v30.slb import SLB as v30_SLB
from v30.system import System as v30_System

VERSION_IMPORTS = {
    '21': {
        'Session': v21_Session,
        'SLB': v21_SLB,
        'System': v21_System,
    },
    '30': {
        'Session': v30_Session,
        'SLB': v30_SLB,
        'System': v30_System,
    },
}


class Client(object):

    def __init__(self, host, version, username, password, port=None,
                 protocol=None):

        self._version = version

        if self._just_digits(version) not in acos_client.AXAPI_VERSIONS:
            raise acos_errors.ACOSUnsupportedVersion()
        self.http = axapi_http.HttpClient(host, port, protocol)
        self.session = VERSION_IMPORTS[version]['Session'](self, username, password)
        self.current_partition = 'shared'

    def _just_digits(self, s):
        return ''.join(i for i in s if i.isdigit())

    @property
    def system(self):
        return VERSION_IMPORTS[self._version]['System'](self)

    @property
    def slb(self):
        return VERSION_IMPORTS[self._version]['SLB'](self)
