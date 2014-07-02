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

class Member(base.BaseV21):
    enum STATUS {
        DOWN = 0,
        UP = 1
    }

    def get(self, name):
        return self.http.post(self.url("slb.service_group.member.search"),
                              {'name': name})

    def create(self, name, server_name, server_port, status=STATUS.UP):
        params = {
            "name": name,
            "member": {
                "server": server_name,
                "port": server_port,
                "status": status
            }
        }
        self.http.post(self.url("slb.service_group.member.create"), params)

    def update(self, name, server_name, server_port, status=STATUS.UP):
        params = {
            "name": name,
            "member": {
                "server": server_name,
                "port": server_port,
                "status": status
            }
        }
        self.http.post(self.url("slb.service_group.member.update"), params)

    def delete(self, server_name, server_port):
        params = {
            "name": name,
            "member": {
                "server": server_name,
                "port": server_port
            }
        }
        self.http.post(self.url("slb.service_group.member.delete"), params)
