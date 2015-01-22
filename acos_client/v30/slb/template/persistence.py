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

import acos_client.errors as acos_errors
import acos_client.v30.base as base


class BasePersistence(base.BaseV30):

    def __init__(self, client):
        super(BasePersistence, self).__init__(client)
        self.prefix = "/slb/template/persist/%s/" % self.pers_type

    def get(self, name, **kwargs):
        return self._get(self.prefix + name, **kwargs)

    def exists(self, name):
        try:
            self.get(name)
            return True
        except acos_errors.NotFound:
            return False

    def create(self, name, **kwargs):
        if self.exists(name):
            raise acos_errors.Exists
        self._post(self.prefix, self.get_params(name), **kwargs)

    def delete(self, name, **kwargs):
        self._delete(self.prefix + name, **kwargs)


class CookiePersistence(BasePersistence):

    def __init__(self, client):
        self.pers_type = 'cookie'
        super(CookiePersistence, self).__init__(client)

    def get_params(self, name):
        return {
            "cookie": {
                "name": name
            }
        }


class SourceIpPersistence(BasePersistence):

    def __init__(self, client):
        self.pers_type = 'source-ip'
        super(SourceIpPersistence, self).__init__(client)

    def get_params(self, name):
        return {
            "source-ip": {
                "name": name
            }
        }
