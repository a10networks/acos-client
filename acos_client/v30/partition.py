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

import random
import time

import acos_client.errors as acos_errors

import base


class Partition(base.BaseV30):

    def available(self):
        return self._get('/partition-available-id/oper/')

    def exists(self, name):
        if name == 'shared':
            return True
        try:
            self._get("/partition/" + name)
            return True
        except acos_errors.NotFound:
            return False

    def active(self, name='shared'):
        if self.client.current_partition != name:
            self._post("/active-partition/" + name)
            self.client.current_partition = name

    def _next_available_id(self):
        a = self.available()
        if a is None:
            raise acos_errors.OutOfPartitions()

        z = a['partition-available-id']['oper']['range-list'][0]['start']
        return int(z)

    def _create(self, name, partition_id):
        params = {
            "partition": {
                "partition-name": name,
                "id": partition_id,
            }
        }
        self._post("/partition", params)

    def create(self, name):
        if name == 'shared':
            return

        # For concurrency's sake, since we have to lookup the id and then
        # set it, loop if we get an exists error.
        for i in xrange(1, 1000):
            try:
                self._create(name, self._next_available_id())
                break
            except acos_errors.PartitionIdExists:
                time.sleep(0.05 + random.random()/100)

    def delete(self, name):
        if name != 'shared':
            self._delete("/partition/" + name)
