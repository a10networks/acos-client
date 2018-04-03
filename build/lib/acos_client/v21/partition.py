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

import acos_client.errors as acos_errors

import base


class Partition(base.BaseV21):

    def exists(self, name):
        if name == 'shared':
            return True
        try:
            self._post("system.partition.search", {'name': name})
            return True
        except acos_errors.NotFound:
            return False

    def active(self, name='shared'):
        if self.client.current_partition != name:
            self._post("system.partition.active", {'name': name})
            self.client.current_partition = name

    def create(self, name):
        params = {
            'partition': {
                'max_aflex_file': 32,
                'network_partition': 0,
                'name': name
            }
        }
        if name != 'shared':
            self._post("system.partition.create", params)

    def delete(self, name):
        if name != 'shared':
            self.client.session.close()
            self._post("system.partition.delete", {"name": name})
