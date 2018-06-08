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

import logging
import six
import socket

import acos_client
from acos_client import errors as acos_errors
from acos_client.v21 import axapi_http as v21_http
from acos_client.v21.dns import DNS as v21_DNS
from acos_client.v21.ha import HA as v21_HA
from acos_client.v21.interface import Interface as v21_Interface
from acos_client.v21.license_manager import LicenseManager as v21_LicenseManager
from acos_client.v21.nat import Nat as v21_Nat
from acos_client.v21.network import Network as v21_Network
from acos_client.v21.session import Session as v21_Session
from acos_client.v21.sflow import SFlow as v21_SFlow
from acos_client.v21.slb import SLB as v21_SLB
from acos_client.v21.system import System as v21_System
from acos_client.v30 import axapi_http as v30_http
from acos_client.v30.dns import DNS as v30_DNS
from acos_client.v30.file import File as v30_File
from acos_client.v30.ha import HA as v30_HA
from acos_client.v30.interface import Interface as v30_Interface
from acos_client.v30.license_manager import LicenseManager as v30_LicenseManager
from acos_client.v30.nat import Nat as v30_Nat
from acos_client.v30.network import Network as v30_Network
from acos_client.v30.session import Session as v30_Session
from acos_client.v30.sflow import SFlow as v30_SFlow
from acos_client.v30.slb import SLB as v30_SLB
from acos_client.v30.system import System as v30_System

VERSION_IMPORTS = {
    '21': {
        'DNS': v21_DNS,
        'http': v21_http,
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
        'DNS': v30_DNS,
        'http': v30_http,
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

LOG = logging.getLogger(__name__)


class Client(object):

    def __init__(self, host, version, username, password, port=None,
                 protocol="https", timeout=None, retry_errno_list=None):
        self._version = self._just_digits(version)
        if self._version not in acos_client.AXAPI_VERSIONS:
            raise acos_errors.ACOSUnsupportedVersion()
        self.host = host
        self.port = port
        self.http = VERSION_IMPORTS[self._version]['http'].HttpClient(
            host, port, protocol, timeout=timeout, retry_errno_list=retry_errno_list)
        self.session = VERSION_IMPORTS[self._version]['Session'](
            self, username, password)
        self.current_partition = 'shared'

    def _just_digits(self, s):
        return ''.join(i for i in str(s) if i.isdigit())

    @property
    def dns(self):
        return VERSION_IMPORTS[self._version]['DNS'](self)

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

    def wait_for_connect(self, max_timeout=60):
        for i in six.moves.range(0, max_timeout):
            try:
                LOG.debug("wait_for_connect: attempting %s", self.host)
                s = socket.create_connection((self.host, self.port), 1.0)
                s.close()
                LOG.debug("wait_for_connect: connected %s", self.host)
                break
            except socket.error:
                pass
