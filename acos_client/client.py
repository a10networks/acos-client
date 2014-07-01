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

from axapi_http import HttpClient
from v21.session import Session
from v21.system import System


class Client(object):

    def __init__(self, host, username, password, port=None, protocol=None):
        self.http = HttpClient(host, port, protocol)
        self.session = Session(self.http, username, password)

    @property
    def system(self):
        return System(self.http, self.session)




    def check_version(self):
        if 'skip_version_check' in self.device_info:
            if self.device_info['skip_version_check']:
                return

        info_url = ("/services/rest/v2.1/?format=json&session_id=%s"
                    "&method=system.information.get" % self.session_id)

        r = self.axapi_http("GET", info_url)

        x = r['system_information']['software_version'].split('.')
        major = int(x[0])
        minor = int(x[1])
        dot = 0
        m = re.match("^(\d+)", x[2])
        if m is not None:
            dot = int(m.group(1))

        if major < 2 or minor < 7 or dot < 2:
            LOG.error(_("A10Client: driver requires ACOS version 2.7.2+"))
            raise a10_ex.A10ThunderVersionMismatch()
