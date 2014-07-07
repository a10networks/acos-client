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

from persistence import CookiePersistence
from persistence import SourceIpPersistence


class Template(base.BaseV21):

    @property
    def cookie_persistence(self):
        return CookiePersistence(self.client)

    @property
    def src_ip_persistence(self):
        return SourceIpPersistence(self.client)
