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
        return Member(self.http, self.session)

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
    STATELESS_PER_PACKAGE_ROUND_ROBIN = 13

    # Valid protocols
    TCP = 2
    UDP = 3

    def get(self, name):
        return self.http.post(self.url("slb.service_group.search"),
                              {'name': name})

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN):
        params = {
            "service_group": {
                "name": name,
                "protocol": protocol,
                "lb_method": lb_method
            }
        }
        self.http.post(self.url("slb.service_group.create"), params)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None):
        params = {
            "service_group": {
                "name": name,
            }
        }
        if protocol is not None:
            params['service_group']['protocol'] = protocol
        if lb_method is not None:
            params['service_group']['lb_method'] = lb_method
        if health_monitor is not None:
            params['service_group']['health_monitor'] = health_monitor

        self.http.post(self.url("slb.service_group.update"), params)

    def delete(self, name):
        self.http.post(self.url("slb.service_group.delete"), {'name': name})


