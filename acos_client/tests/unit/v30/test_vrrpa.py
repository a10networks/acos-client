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

    def expected_payload(self, vrid_val, threshold=1, disable=0, floating_ips=[]):
        rv = {
            'vrid': {
                'vrid-val': vrid_val,
                'preempt-mode': {
                    'threshold': threshold,
                    'disable': disable
                }
            }
        }

        if len(floating_ips) > 0:
            rv["vrid"]["floating-ip"] = floating_ips

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

    def test_vrid_update_threshold(self):
        self.target.update(4, threshold=2)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, threshold=2), mock.ANY)

    def test_vrid_update_disable(self):
        self.target.update(4, disable=1)
        self.client.http.request.assert_called_with(
            "PUT", self.url_prefix + '4', self.expected_payload(4, disable=1), mock.ANY)

    def test_vrid_create_floatingip(self):
        expected = {'ip-address-cfg': [{'ip-address': u'1.2.3.4'}]}
        self.target.create(4, disable=1, floating_ips=["1.2.3.4"])
        self.client.http.request.assert_called_with(
            "POST", self.url_prefix, self.expected_payload(4, disable=1, floating_ips=expected), mock.ANY)        
