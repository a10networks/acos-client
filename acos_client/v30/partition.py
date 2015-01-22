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

    # def _part_id(self, name):
    #     return int(name[:4])

    # def _part_name(self, name, id):
    #     return ("%04d_%s" % (id, name))[0:13]

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

        if self.exists(name):
            raise acos_errors.Exists

        # For concurrency's sake, since we have to lookup the id and then
        # set it, loop if we get an exists error.
        for i in xrange(1, 1000):
            try:
                self._create(name, self._next_available_id())
                break
            except acos_errors.PartitionIdExists:
                time.sleep(0.05 + random.random()/100)

    def delete(self, name):
        if name == 'shared':
            return

        self.client.session.close()
        try:
            p = self._get("/partition/" + name)
        except acos_errors.NotFound:
            return
        try:
            self._delete("/partition/" + name)
        except acos_errors.NotFound:
            pass

        self.client.session.close()
        self._post("/delete/partition", p)

        self.client.session.close()
