# Copyright 2016, A10 Networks
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

from acos_client.v30 import base


class BladeParameters(base.BaseV30):
    def __init__(self, client):
        super(BladeParameters, self).__init__(client)
        self.base_url = "/vrrp-a/vrid/{0}/blade-parameters"
        self.interfaces = {'interface': []}
        self.gateways = {
            'gateway': {
                'ipv4-gateway-list': [],
                'ipv6-gateway-list': []
            }
        }

    def _build_params(self, priority=None, **kwargs):
        rv = {'blade-parameters': {}}
        if priority:
            priority = priority if priority in range(1, 256) else 150
            rv['blade-parameters']['priority'] = priority

        if self.interfaces['interface']:
            rv['blade-parameters']['tracking-options'] = self.interfaces

        if self.gateways['gateway']['ipv4-gateway-list']:
            if rv['blade-parameters'].get('tracking-options'):
                rv['blade-parameters']['tracking-options'].update(self.gateways)
            else:
                rv['blade-parameters']['tracking-options'] = self.gateways

        if self.gateways['gateway']['ipv6-gateway-list']:
            if rv['blade-parameters'].get('tracking-options'):
                if rv['blade-parameters']['tracking-options'].get('gateway'):
                    rv['blade-parameters']['tracking-options']['gateway'].update(self.gateways)
                else:
                    rv['blade-parameters']['tracking-options'] = self.gateways
            else:
                rv['blade-parameters']['tracking-options'] = self.gateways
        return rv

    def add_interface(self, ethernet=1, priority_cost=1):
        interface = {
            'ethernet': ethernet,
            'priority-cost': priority_cost
        }
        self.interfaces['interface'].append(interface)

    def add_ipv4gateway(self, ip_address, priority_cost=1):
        gateway = {
            'ip-address': ip_address,
            'priority-cost': priority_cost
        }
        self.gateways['gateway']['ipv4-gateway-list'].append(gateway)

    def add_ipv6gateway(self, ip_address, priority_cost=1):
        gateway = {
            'ip-address': ip_address,
            'priority-cost': priority_cost
        }
        self.gateways['gateway']['ipv6-gateway-list'].append(gateway)

    def get(self, vrid_val):
        return self._get(self.base_url.format(vrid_val))

    def create(self, vrid_val, priority=None, **kwargs):
        payload = self._build_params(priority, **kwargs)
        self._post(self.base_url.format(vrid_val), payload)

    def update(self, vrid_val, priority=None, **kwargs):
        payload = self._build_params(priority, **kwargs)
        self._put(self.base_url.format(vrid_val), payload)

    def delete(self, vrid_val):
        return self._delete(self.base_url.format(vrid_val))
