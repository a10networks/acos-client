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

import acos_client.errors as acos_errors
import acos_client.v30.base as base

from member import Member


class ServiceGroup(base.BaseV30):
    url_prefix = '/slb/service-group/'

    @property
    def member(self):
        return Member(self.client)

    # Valid LB methods
    ROUND_ROBIN = 'round-robin'
    WEIGHTED_ROUND_ROBIN = 'weighted-rr'
    LEAST_CONNECTION = 'least-connection'
    WEIGHTED_LEAST_CONNECTION = 'weighted-least-connection'
    LEAST_CONNECTION_ON_SERVICE_PORT = 'service-least-connection'
    WEIGHTED_LEAST_CONNECTION_ON_SERVICE_PORT = \
        'service-weighted-least-connection'
    FAST_RESPONSE_TIME = 'fastest-response'
    LEAST_REQUEST = 'least-request'
    STRICT_ROUND_ROBIN = 'round-robin-strict'
    STATELESS_SOURCE_IP_HASH = 'stateless-src-ip-hash'
    STATELESS_SOURCE_IP_HASH_ONLY = 'stateless-src-ip-only-hash'
    STATELESS_DESTINATION_IP_HASH = 'stateless-dst-ip-hash'
    STATELESS_SOURCE_DESTINATION_IP_HASH = 'stateless-src-dst-ip-hash'
    STATELESS_PER_PACKET_ROUND_ROBIN = 'stateless-per-pkt-round-robin'

    # Valid protocols
    TCP = 'tcp'
    UDP = 'udp'

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def _set(self, name, protocol=None, lb_method=None, hm_name=None,
             update=False, **kwargs):

        # Normalize "" -> None for json
        hm_name = hm_name or None

        # v30 needs unit tests badly...

        params = {
            "service-group": self.minimal_dict({
                "name": name,
                "protocol": protocol,
            })
        }

        # If we explicitly disable health checks, ensure it happens
        # Else, we implicitly disable health checks if not specified.
        health_check_disable = 1 if kwargs.get("health_check_disable", False) else 0

        # When enabling/disabling a health monitor, you can't specify
        # health-check-disable and health-check at the same time.
        if hm_name is None:
            params["service-group"]["health-check-disable"] = health_check_disable
        else:
            params["service-group"]["health-check"] = hm_name

        if lb_method is None:
            pass
        elif lb_method[-16:] == 'least-connection':
            params['service-group']['lc-method'] = lb_method
        elif lb_method[:9] == 'stateless':
            params['service-group']['stateless-lb-method'] = lb_method
        else:
            params['service-group']['lb-method'] = lb_method

        if not update:
            name = ''

        self._post(self.url_prefix + name, params, **kwargs)

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN, **kwargs):
        try:
            self.get(name)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists

        self._set(name, protocol, lb_method, **kwargs)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None,
               **kwargs):
        self._set(name, protocol, lb_method,
                  health_monitor, update=True, **kwargs)

    def delete(self, name):
        self._delete(self.url_prefix + name)

    def stats(self, name, *args, **kwargs):
        return self._get(self.url_prefix + name + "/stats", **kwargs)
