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


class VirtualService(base.BaseV21):

    def all(self, **kwargs):
        return self._get("slb.virtual_service.getAll", **kwargs)

    def get(self, name, **kwargs):
        return self._post("slb.virtual_service.search", {'name': name},
                          **kwargs)

    def _set(self, action, name, protocol, port, **kwargs):
        params = {
            "virtual_service": {
                "port": port,
                "protocol": protocol,
                "name": name
            }
        }

        return self._post(action, params, **kwargs)

    def create(self, name, protocol, port, **kwargs):
        return self._set("slb.virtual_service.create", name, protocol, port,
                         **kwargs)

    def update(self, name, protocol, port, **kwargs):
        return self._set("slb.virtual_service.update", name, protocol, port,
                         **kwargs)

    def delete(self, name, **kwargs):
        return self._post("slb.virtual_service.delete", {"name": name},
                          **kwargs)

    def all_delete(self, **kwargs):
        return self._get("slb.virtual_service.deleteAll", **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.virtual_service.fetchStatistics",
                          {"name": name}, **kwargs)

    def all_stats(self, **kwargs):
        return self._get("slb.virtual_service.fetchAllStatistics", **kwargs)
