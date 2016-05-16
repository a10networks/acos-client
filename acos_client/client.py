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

import errors as acos_errors
import v21.axapi_http
from v21.ha import HA as v21_HA
from v21.interface import Interface as v21_Interface
from v21.license_manager import LicenseManager as v21_LicenseManager
from v21.nat import Nat as v21_Nat
from v21.network import Network as v21_Network
from v21.session import Session as v21_Session
from v21.sflow import SFlow as v21_SFlow
from v21.slb import SLB as v21_SLB
from v21.system import System as v21_System

import v30.axapi_http
from v30.file import File as v30_File
from v30.ha import HA as v30_HA
from v30.interface import Interface as v30_Interface
from v30.license_manager import LicenseManager as v30_LicenseManager
from v30.nat import Nat as v30_Nat
from v30.network import Network as v30_Network
from v30.session import Session as v30_Session
from v30.sflow import SFlow as v30_SFlow
from v30.slb import SLB as v30_SLB
from v30.system import System as v30_System

VERSION_IMPORTS = {
    '21': {
        'http': v21.axapi_http,
        'HA': v21_HA,
        'Interface': v21_Interface,
        'LicenseManager': v21_LicenseManager,
        'Nat': v21_Nat,
        'Network': v21_Network,
        'Session': v21_Session,
        'SFlow': v21_SFlow,
        'SLB': v21_SLB,
        'System': v21_System,
    },
    '30': {
        'http': v30.axapi_http,
        'Interface': v30_Interface,
        'HA': v30_HA,
        'LicenseManager': v30_LicenseManager,
        'Nat': v30_Nat,
        'Network': v30_Network,
        'Session': v30_Session,
        'SFlow': v30_SFlow,
        'SLB': v30_SLB,
        'System': v30_System,
        'File': v30_File
    },
}


class Client(object):

    def __init__(self, host, version, username, password, port=None,
                 protocol="https", timeout=None, retry_errno_list=None):
        self._version = self._just_digits(version)
        if self._version not in acos_client.AXAPI_VERSIONS:
            raise acos_errors.ACOSUnsupportedVersion()
        self.http = VERSION_IMPORTS[self._version]['http'].HttpClient(
            host, port, protocol, timeout=timeout, retry_errno_list=retry_errno_list)
        self.session = VERSION_IMPORTS[self._version]['Session'](
            self, username, password)
        self.current_partition = 'shared'

    def _just_digits(self, s):
        return ''.join(i for i in str(s) if i.isdigit())

    @property
    def ha(self):
        return VERSION_IMPORTS[self._version]['HA'](self)

    @property
    def interface(self):
        return VERSION_IMPORTS[self._version]['Interface'](self)

    @property
    def system(self):
        return VERSION_IMPORTS[self._version]['System'](self)

    @property
    def slb(self):
        return VERSION_IMPORTS[self._version]['SLB'](self)

    @property
    def network(self):
        return VERSION_IMPORTS[self._version]['Network'](self)

    @property
    def nat(self):
        return VERSION_IMPORTS[self._version]['Nat'](self)

    @property
    def file(self):
        return VERSION_IMPORTS[self._version]['File'](self)

    @property
    def sflow(self):
        return VERSION_IMPORTS[self._version]['SFlow'](self)

    @property
    def license_manager(self):
        return VERSION_IMPORTS[self._version]["LicenseManager"](self)
