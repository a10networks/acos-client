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
from member import Member


class ServiceGroup(base.BaseV30):
    url_prefix = '/slb/service-group/'

    @property
    def member(self):
        return Member(self.client)

    # Valid LB methods
    ROUND_ROBIN = 'round-robin' 
    WEIGHTED_ROUND_ROBIN = 1
    LEAST_CONNECTION = 'least-request'
    WEIGHTED_LEAST_CONNECTION = 3
    LEAST_CONNECTION_ON_SERVICE_PORT = 4
    WEIGHTED_LEAST_CONNECTION_ON_SERVICE_PORT = 5
    FAST_RESPONSE_TIME = 'fastest-response'
    LEAST_REQUEST = 'least-request'
    STRICT_ROUND_ROBIN = 'round-robin-strict'
    STATELESS_SOURCE_IP_HASH = 9
    STATELESS_SOURCE_IP_HASH_ONLY = 10
    STATELESS_DESTINATION_IP_HASH = 11
    STATELESS_SOURCE_DESTINATION_IP_HASH = 12
    STATELESS_PER_PACKAGE_ROUND_ROBIN = 13

    # Valid protocols
    TCP = 'tcp'
    UDP = 'udp'

    def get(self, name):
        return self._get(self.url_prefix + name)

    def _set(self, name, protocol=None, lb_method=None, hm_name=None, update=False):
        params = {
            "service-group": self.minimal_dict({
                "name": name,
                "protocol": protocol,
                "lb-method": lb_method,
                "health-monitor": hm_name
            })
        }

        if not update:
            name = ''

        self._post(self.url_prefix + name, params)

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN):
        self._set(name, protocol, lb_method)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None):
        self._set(name, protocol, lb_method,
                  health_monitor, update=True)

    def delete(self, name):
        self._delete(self.url_prefix + name)
