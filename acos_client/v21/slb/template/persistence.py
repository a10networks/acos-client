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

from acos_client import errors as acos_errors
from acos_client.v21 import base


class BasePersistence(base.BaseV21):

    def __init__(self, client):
        super(BasePersistence, self).__init__(client)
        self.prefix = "slb.template.%s_persistence" % self.pers_type

    def get(self, name, **kwargs):
        return self._post(("%s.search" % self.prefix), {'name': name},
                          **kwargs)

    def exists(self, name, **kwargs):
        try:
            self.get(name, **kwargs)
            return True
        except acos_errors.NotFound:
            return False

    def create(self, name, **kwargs):
        self._post(("%s.create" % self.prefix), self.get_params(name),
                   **kwargs)

    def delete(self, name, **kwargs):
        self._post(("%s.delete" % self.prefix), {'name': name}, **kwargs)


class CookiePersistence(BasePersistence):

    def __init__(self, client):
        self.pers_type = 'cookie'
        super(CookiePersistence, self).__init__(client)

    def get_params(self, name):
        return {
            "cookie_persistence_template": {
                "name": name
            }
        }


class SourceIpPersistence(BasePersistence):

    def __init__(self, client):
        self.pers_type = 'src_ip'
        super(SourceIpPersistence, self).__init__(client)

    def get_params(self, name):
        return {
            "src_ip_persistence_template": {
                "name": name
            }
        }
