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

from member import Member


class ServiceGroup(base.BaseV21):

    @property
    def member(self):
        return Member(self.client)

    # Valid LB methods
    ROUND_ROBIN = 0
    WEIGHTED_ROUND_ROBIN = 1
    LEAST_CONNECTION = 2
    WEIGHTED_LEAST_CONNECTION = 3
    LEAST_CONNECTION_ON_SERVICE_PORT = 4
    WEIGHTED_LEAST_CONNECTION_ON_SERVICE_PORT = 5
    FAST_RESPONSE_TIME = 6
    LEAST_REQUEST = 7
    STRICT_ROUND_ROBIN = 8
    STATELESS_SOURCE_IP_HASH = 9
    STATELESS_SOURCE_IP_HASH_ONLY = 10
    STATELESS_DESTINATION_IP_HASH = 11
    STATELESS_SOURCE_DESTINATION_IP_HASH = 12
    STATELESS_PER_PACKET_ROUND_ROBIN = 13

    # Valid protocols
    TCP = 2
    UDP = 3

    def get(self, name, **kwargs):
        return self._post("slb.service_group.search", {'name': name}, **kwargs)

    def _set(self, action, name, protocol=None, lb_method=None, hm_name=None,
             **kwargs):
        params = {
            "service_group": self.minimal_dict({
                "name": name,
                "protocol": protocol,
                "lb_method": lb_method,
                "health_monitor": hm_name
            })
        }
        self._post(action, params, **kwargs)

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN, **kwargs):
        self._set("slb.service_group.create", name, protocol, lb_method,
                  **kwargs)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None,
               **kwargs):
        self._set("slb.service_group.update", name, protocol, lb_method,
                  health_monitor, **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.service_group.delete", {'name': name}, **kwargs)

    def all(self, **kwargs):
        return self._get('slb.service_group.getAll', **kwargs)

    def all_delete(self, **kwargs):
        self._get('slb.service_group.deleteAll', **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.service_group.fetchStatistics",
                          {"name": name}, **kwargs)
