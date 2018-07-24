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

from acos_client.v21 import base


class Member(base.BaseV21):

    def _write(self, action, service_group_name, server_name, server_port,
               status=None, **kwargs):
        params = {
            "name": service_group_name,
            "member": self.minimal_dict({
                "server": server_name,
                "port": int(server_port),
                "status": status
            })
        }
        self._post(action, params, **kwargs)

    def create(self, service_group_name, server_name, server_port, status=1,
               **kwargs):
        self._write("slb.service_group.member.create", service_group_name,
                    server_name, server_port, status, **kwargs)

    def update(self, service_group_name, server_name, server_port, status=1,
               **kwargs):
        self._write("slb.service_group.member.update", service_group_name,
                    server_name, server_port, status, **kwargs)

    def delete(self, service_group_name, server_name, server_port, **kwargs):
        self._write("slb.service_group.member.delete", service_group_name,
                    server_name, int(server_port), **kwargs)

    def get_oper(self, service_group_name, server_name, server_port, **kwargs):
        sg_stats = self._post("slb.service_group.fetchStatistics",
                              {"name": service_group_name}, **kwargs)
        members_stats = sg_stats["service_group_stat"]["member_stat_list"]
        member_stats = filter(lambda x: x.get("server") == server_name, members_stats)
        return member_stats
