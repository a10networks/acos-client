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
import acos_client.v21.base as base


class Partition(base.BaseV21):

    def search(self, name):
        r = self.http.post(self.url("system.partition.search"), {'name': name})
        raise "need to fix here"
        #     if 'response' in response:
        #         if "err" in response['response']:
        #             if response['response']['err'] == 520749062:
        #                 return False
        #     elif "partition" in response:
        #         return True
        return False

    def active(self, name='shared'):
        self.http.post(self.url("system.partition.search"), {'name': name})

    def create(self, name):
        params = {
            'partition': {
                'max_aflex_file': 32,
                'network_partition': 0,
                'name': name
            }
        }
        self.http.post(self.url("system.partition.create"), params)

    def delete(self, name):
        self.client.session.close()
        self.http.post(self.url("system.partition.delete"), {"name": name})
