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

    def expected_payload(self, vrid_val, threshold=1, disable=0, floating_ip=None,
                         is_partition=None):
        rv = {
            'vrid': {
                'vrid-val': vrid_val,
                'preempt-mode': {
                    'threshold': threshold,
                    'disable': disable
                }
            }
        }
        if floating_ip:
            fip_config_json = None
            if is_partition:
                fip_config_json = {
                    'ip-address-part-cfg': [{
                        'ip-address-partition': floating_ip
                    }]}
            else:
                fip_config_json = {
                    'ip-address-cfg': [{
                        'ip-address': floating_ip
                    }]}

            rv['vrid']['floating-ip'] = fip_config_json
        return rv

    def test_vrid_get(self):
        self.target.get(0)
        self.client.http.request.assert_called_with("GET", self.url_prefix + '0', {}, mock.ANY)

    def test_vrid_create_threshold(self):
        self.target.create(4, threshold=2)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, threshold=2), mock.ANY)

    def test_vrid_create_disable(self):
        self.target.create(4, disable=1)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, disable=1), mock.ANY)

    def test_vrid_create_floating_ip(self):
        self.target.create(4, threshold=1, disable=0, floating_ip='10.10.10.8')
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, floating_ip='10.10.10.8'),
            mock.ANY)

    def test_vrid_update_threshold(self):
        self.target.update(4, threshold=2)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, threshold=2), mock.ANY)

    def test_vrid_update_disable(self):
        self.target.update(4, disable=1)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, disable=1), mock.ANY)

    def test_vrid_update_floating_ip(self):
        self.target.update(4, threshold=1, disable=0, floating_ip='10.10.10.9')
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, floating_ip='10.10.10.9'),
            mock.ANY)

    def test_patition_vrid_create_floating_ip(self):
        self.target.create(4, threshold=1, disable=0, floating_ip='10.10.10.8', is_partition=True)
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, floating_ip='10.10.10.8',
                                                           is_partition=True), mock.ANY)

    def test_partition_vrid_update_floating_ip(self):
        self.target.update(4, threshold=1, disable=0, floating_ip='10.10.10.9', is_partition=True)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, floating_ip='10.10.10.9',
                                                                is_partition=True), mock.ANY)
