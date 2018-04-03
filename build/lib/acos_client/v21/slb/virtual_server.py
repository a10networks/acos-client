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

from virtual_port import VirtualPort


class VirtualServer(base.BaseV21):

    @property
    def vport(self):
        return VirtualPort(self.client)

    def all(self, **kwargs):
        return self._get("slb.virtual_server.getAll", **kwargs)

    def get(self, name, **kwargs):
        return self._post("slb.virtual_server.search", {'name': name},
                          **kwargs)

    def _set(self, action, name, ip_address=None, status=1, vrid=None, **kwargs):
        params = {
            "virtual_server": self.minimal_dict({
                "name": name,
                "address": ip_address,
                "status": status,
            }),
        }
        if vrid:
            params['virtual_server']['vrid'] = vrid

        return self._post(action, params, **kwargs)

    def create(self, name, ip_address, status=1, vrid=None, **kwargs):
        return self._set("slb.virtual_server.create", name, ip_address, status,
                         vrid=vrid, **kwargs)

    def update(self, name, ip_address=None, status=1, vrid=None, **kwargs):
        return self._set("slb.virtual_server.update", name, ip_address, status,
                         vrid=vrid, **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.virtual_server.delete", {"name": name}, **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.virtual_server.fetchStatistics", {"name": name},
                          **kwargs)

    def all_stats(self, **kwargs):
        return self._get("slb.virtual_server.fetchAllStatistics", **kwargs)
