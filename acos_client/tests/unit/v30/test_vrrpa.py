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

from acos_client.v30.vrrpa import vrid


class TestVRID(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = vrid.VRID(self.client)
        self.url_prefix = "/axapi/v3/vrrp-a/vrid/"

    def expected_payload(self, vrid_val, threshold=1, disable=0, is_partition=None):
        rv = {
            'vrid': {
                'vrid-val': vrid_val,
                'preempt-mode': {
                    'threshold': threshold,
                    'disable': disable
                }
            }
        }
        return rv

    def test_vrid_get(self):
        self.target.get(0)
        self.client.http.request.assert_called_with("GET", self.url_prefix + '0', {}, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_create_threshold(self):
        self.target.create(4, threshold=2)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, threshold=2), mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_create_disable(self):
        self.target.create(4, disable=1)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, disable=1), mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_create_floating_ip(self):
        self.target.create(4, threshold=1, disable=0, floating_ips=['10.10.10.8'])
        payload = self.expected_payload(4)
        payload['vrid']['floating-ip'] = mock.ANY
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, payload, mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_update_threshold(self):
        self.target.update(4, threshold=2)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, threshold=2), mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_update_disable(self):
        self.target.update(4, disable=1)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, disable=1), mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_vrid_update_floating_ip(self):
        self.target.update(4, threshold=1, disable=0, floating_ips=['10.10.10.9'])
        payload = self.expected_payload(4)
        payload['vrid']['floating-ip'] = mock.ANY
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', payload,
            mock.ANY, axapi_args=None, max_retries=None, timeout=None)

    def test_patition_vrid_create_floating_ip(self):
        self.target.create(4, threshold=1, disable=0, floating_ips=['10.10.10.8'], is_partition=True)
        payload = self.expected_payload(4, is_partition=True)
        payload['vrid']['floating-ip'] = mock.ANY
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, payload, mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_partition_vrid_update_floating_ip(self):
        self.target.update(4, threshold=1, disable=0, floating_ips=['10.10.10.9'], is_partition=True)
        payload = self.expected_payload(4, is_partition=True)
        payload['vrid']['floating-ip'] = mock.ANY
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', payload, mock.ANY,
            axapi_args=None, max_retries=None, timeout=None)

    def test_build_params_multi_ip(self):
        floating_ips = ['11.11.11.11', '12.12.12.12', '13.13.13.13']
        floating_ip_payload = [{'ip-address': '11.11.11.11'},
                               {'ip-address': '12.12.12.12'},
                               {'ip-address': '13.13.13.13'}]
        payload = self.target._build_params(0, floating_ips=floating_ips)
        ip_cfg = list(payload['vrid']['floating-ip']['ip-address-cfg'])
        self.assertEqual(floating_ip_payload, ip_cfg)

    def test_build_params_multi_ip_partition(self):
        floating_ips = ['11.11.11.11', '12.12.12.12', '13.13.13.13']
        floating_ip_payload = [{'ip-address-partition': '11.11.11.11'},
                               {'ip-address-partition': '12.12.12.12'},
                               {'ip-address-partition': '13.13.13.13'}]
        payload = self.target._build_params(0, floating_ips=floating_ips, is_partition=True)
        ip_cfg = list(payload['vrid']['floating-ip']['ip-address-part-cfg'])
        self.assertEqual(floating_ip_payload, ip_cfg)
