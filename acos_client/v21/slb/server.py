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
from acos_client.v21.slb.port import Port


class Server(base.BaseV21):

    def get(self, name, **kwargs):
        return self._post("slb.server.search", {'name': name}, **kwargs)

    def create(self, name, ip_address, status=1, **kwargs):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
                "status": status,
                "conn_resume": kwargs.get("conn_resume", 0),
                "conn_limit": kwargs.get("conn_limit", 8000000),
            }
        }
        self._post("slb.server.create", params, **kwargs)

    def update(self, name, ip_address, status=1, **kwargs):
        params = {
            "server": {
                "name": name,
                "host": ip_address,
                "status": status,
                "conn_resume": kwargs.get("conn_resume", 0),
                "conn_limit": kwargs.get("conn_limit", 8000000),
            }
        }
        self._post("slb.server.update", params, **kwargs)

    def fetchStatistics(self, name, **kwargs):
        return self._post("slb.server.fetchStatistics", {"name": name},
                          **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.server.delete", {"server": {"name": name}}, **kwargs)

    def all(self, **kwargs):
        return self._get('slb.server.getAll', **kwargs)

    def all_delete(self, **kwargs):
        self._get('slb.server.deleteAll', **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.server.fetchStatistics",
                          {"server": {"name": name}}, **kwargs)

    def all_stats(self, **kwargs):
        return self._get('fetchAllStatistics', **kwargs)

    @property
    def port(self):
        return Port(self.client)
