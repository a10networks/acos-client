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


class Server(base.BaseV21):

    def get(self, name):
        return self.http.post(self.url("slb.server.search"),
                              {'name': name})

    def create(self, name, ip_address):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
            }
        }
        self.http.post(self.url("slb.server.create"), params)

    def delete(self, name):
        self.http.post(self.url("slb.server.delete"),
                       {"server": {"name": name}})
