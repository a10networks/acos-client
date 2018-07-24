# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

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

try:
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client.v30.vrrpa import blade_params


class TestBlade(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = blade_params.BladeParameters(self.client)
        self.url_prefix = "/axapi/v3/vrrp-a/vrid/{0}/blade-parameters"

    def _expected_payload(self, priority=None, interface=None, gateway=None):
        rv = {'blade-parameters': {}}
        if priority:
            rv['blade-parameters']['priority'] = priority

        if interface:
            rv['blade-parameters']['tracking-options'] = interface

        if gateway:
            if rv['blade-parameters'].get('tracking-options'):
                rv['blade-parameters']['tracking-options'].update(gateway)
            else:
                rv['blade-parameters']['tracking-options'] = gateway

        return rv

    def _build_interface(self, ethernet=1, priority_cost=1):
        rv = {
            'interface': [{
                'ethernet': ethernet,
                'priority-cost': priority_cost
            }]
        }
        return rv

    def _build_ipv4gateway(self, ip_address, priority_cost=1):
        rv = {
            'gateway': {
                'ipv4-gateway-list': [{
                    'ip-address': ip_address,
                    'priority-cost': priority_cost
                }],
                'ipv6-gateway-list': []
            }
        }
        return rv

    def _build_ipv6gateway(self, ip_address, priority_cost=1):
        rv = {
            'gateway': {
                'ipv6-gateway-list': [{
                    'ip-address': ip_address,
                    'priority-cost': priority_cost
                }],
                'ipv4-gateway-list': []
            }
        }
        return rv

    def test_blade_get(self):
        self.target.get(0)
        self.client.http.request.assert_called_with("GET", self.url_prefix.format(0), {}, mock.ANY)

    def test_blade_create(self):
        self.target.create(4)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(), mock.ANY)

    def test_blade_create_priority(self):
        self.target.create(4, 122)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(122), mock.ANY)

    def test_blade_create_interface(self):
        interface = self._build_interface()

        self.target.add_interface()
        self.target.create(4)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(interface=interface), mock.ANY)

    def test_blade_create_gateway(self):
        gateway = self._build_ipv4gateway('1.1.1.1')

        self.target.add_ipv4gateway('1.1.1.1')
        self.target.create(4)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(gateway=gateway), mock.ANY)

    def test_blade_create_gateway_ipv6(self):
        gateway = self._build_ipv6gateway('1.1.1.1')

        self.target.add_ipv6gateway('1.1.1.1')
        self.target.create(4)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(gateway=gateway), mock.ANY)

    def test_blade_create_interface_gateway(self):
        interface = self._build_interface()
        gateway = self._build_ipv4gateway('1.1.1.1')

        self.target.add_interface()
        self.target.add_ipv4gateway('1.1.1.1')
        self.target.create(4)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix.format(4),
            self._expected_payload(interface=interface, gateway=gateway), mock.ANY)

    def test_blade_update(self):
        self.target.update(4)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(), mock.ANY)

    def test_blade_update_priority(self):
        self.target.update(4, 122)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(122), mock.ANY)

    def test_blade_update_interface(self):
        interface = self._build_interface()

        self.target.add_interface()
        self.target.update(4)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(interface=interface), mock.ANY)

    def test_blade_update_gateway(self):
        gateway = self._build_ipv4gateway('1.1.1.1')

        self.target.add_ipv4gateway('1.1.1.1')
        self.target.update(4)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(gateway=gateway), mock.ANY)

    def test_blade_update_gateway_ipv6(self):
        gateway = self._build_ipv6gateway('1.1.1.1')

        self.target.add_ipv6gateway('1.1.1.1')
        self.target.update(4)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(gateway=gateway), mock.ANY)

    def test_blade_update_interface_gateway(self):
        interface = self._build_interface()
        gateway = self._build_ipv4gateway('1.1.1.1')

        self.target.add_interface()
        self.target.add_ipv4gateway('1.1.1.1')
        self.target.update(4)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix.format(4),
            self._expected_payload(interface=interface, gateway=gateway), mock.ANY)
