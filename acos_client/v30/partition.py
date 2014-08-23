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

import base


class Partition(base.BaseV30):

    def exists(self, name):
        try:
            self._get("/partition/" + name)
            return True
        except acos_errors.NotFound:
            return False

    def active(self, name='shared'):

        if self.client.current_partition != name:
            self._post("/active-partition/" + name)
            self.client.current_partition = name

    def create(self, name, p_id=2):
        if name != 'shared':
            params = {
                "partition": {
                    "id": p_id,
                    "partition-name": name
                }
            }
            self._post("/partition", params)

    def delete(self, name):
        if name != 'shared':
            self._delete("/delete/partition/" + name)
