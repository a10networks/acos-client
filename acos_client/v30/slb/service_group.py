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
    SOURCE_IP_HASH_ONLY = 'src-ip-only-hash'
    SOURCE_IP_HASH = 'src-ip-hash'
    DESTINATION_IP_HASH_ONLY = 'dst-ip-only-hash'
    DESTINATION_IP_HASH = 'dst-ip-hash'

    # Valid protocols
    TCP = 'tcp'
    UDP = 'udp'

    def get(self, name, **kwargs):
        return self._get(self.url_prefix + name, **kwargs)

    def _build_params(self, name, protocol=None, lb_method=None,
                      health_monitor=None, update=False, **kwargs):

        # Normalize "" -> None for json
        health_monitor = health_monitor or None

        # v30 needs unit tests badly...
        params = {
            "service-group": {
                "name": name,
                "protocol": protocol,
            }
        }

        # If we explicitly disable health checks, ensure it happens
        # Else, we implicitly disable health checks if not specified.
        health_check_disable = 1 if kwargs.get("health_check_disable", False) else 0

        # When enabling/disabling a health monitor, you can't specify
        # health-check-disable and health-check at the same time.
        if health_monitor is None:
            params["service-group"]["health-check-disable"] = health_check_disable
        else:
            params["service-group"]["health-check"] = health_monitor

        if lb_method is None:
            pass
        elif lb_method[-16:] == 'least-connection':
            params['service-group']['lc-method'] = lb_method
            params['service-group']['stateless-auto-switch'] = 0
        elif lb_method[:9] == 'stateless':
            params['service-group']['stateless-lb-method'] = lb_method
        else:
            params['service-group']['lb-method'] = lb_method
            params['service-group']['stateless-auto-switch'] = 0

        return params

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN, **kwargs):
        try:
            self.get(name)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists

        params = self._build_params(name, protocol, lb_method, **kwargs)
        self._post(self.url_prefix + name, params, **kwargs)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None,
               **kwargs):
        old_sg = self.get(name)
        if old_sg['service-group'].get('health-check'):
            del old_sg['service-group']['health-check']
        else:
            del old_sg['service-group']['health-check-disable']

        params = self._build_params(name, protocol, lb_method,
                                    health_monitor, update=True,
                                    **kwargs)

        for k,v in params['service-group'].items():
            if k == "protocol" and v == None:
                params['service-group'][k] = old_sg['service-group'][k]
            if k in ['lb-method', 'lc-method']:
                if not old_sg['service-group'].get(k):
                    if k == 'lb-method':
                        k = 'lc-method'
                    if k == 'lc-method':
                        k = 'lb-method'
            if old_sg['service-group'].get(k) != None:
                del old_sg['service-group'][k]

        self._put(self.url_prefix + name, params, old_sg, **kwargs)
 

    def delete(self, name):
        self._delete(self.url_prefix + name)

    def stats(self, name, *args, **kwargs):
        return self._get(self.url_prefix + name + "/stats", **kwargs)

    def oper(self, name, *args, **kwargs):
        return self._get(self.url_prefix + name + "/oper", **kwargs)
