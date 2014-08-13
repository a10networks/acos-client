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

import acos_client.v30.base as base


class Member(base.BaseV30):

    url_tmpl = '/slb/service-group/{gname}/member/{name}+{port}/'

    def _write(self, action,
               service_group_name,
               server_name,
               server_port,
               status=None):
        params = {
            "member": self.minimal_dict({
                "server": server_name,
                "port": int(server_port),
                "status": status
            })
        }

        url = self.url_tmpl.format(
            gname=service_group_name,
            name=server_name,
            port=server_port
        )
        action(self.url(url), params)

    def create(self, service_group_name, server_name, server_port, status=1):
        self._write(self.http.post, service_group_name,
                    server_name, server_port, status)

    def update(self, service_group_name, server_name, server_port, status=1):
        self._write(self.http.post, service_group_name,
                    server_name, server_port, status)

    def delete(self, service_group_name, server_name, server_port):
        self._write(self.http.delete,  service_group_name,
                    server_name, server_port)
