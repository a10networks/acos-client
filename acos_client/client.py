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
from v21.partition import Partition
from v21.session import Session
from v21.slb import SLB
from v21.system import System


class Client(object):

    def __init__(self, host, username, password, port=None, protocol=None):
        self.http = HttpClient(host, port, protocol)
        self.session = Session(self.http, username, password)
        # self.partition = todo

    def close_session(self):
        if self.session.session_id is None:
            return

        try:
            self.partiion.active()
        except Exception as e:
            pass

        self.session.close()

    @property
    def partition(self):
        return Partition(self)

    @property
    def system(self):
        return System(self)

    @property
    def slb(self):
        return SLB(self)