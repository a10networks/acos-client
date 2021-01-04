# Copyright (C) 2016, A10 Networks Inc. All rights reserved.
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
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client.v30 import vlan


class TestVlan(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = vlan.Vlan(self.client)
        self.url_prefix = "/axapi/v3/network/vlan"
        self.vlan_id = 1
        self.expected_payload = {"vlan": {"vlan-num": self.vlan_id}}

    def test_interface_get_list(self):
        self.target.get_list()
        self.client.http.request.assert_called_with("GET", self.url_prefix, {}, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_interface_get(self):
        self.target.get(self.vlan_id)
        self.client.http.request.assert_called_with(
            "GET", '{0}/{1}'.format(self.url_prefix, self.vlan_id), {}, mock.ANY,
            axapi_args=None, max_retries=None, timeout=None
        )

    def test_vlan_create_shared(self):
        self.target.create(self.vlan_id, shared_vlan=True, untagged_eths=[], untagged_trunks=[],
                           tagged_eths=[], tagged_trunks=[], veth=False, lif=None)

        ep = self.expected_payload
        ep['vlan']['shared-vlan'] = True
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_untagged_eths(self):
        untagged_eths = [{'untagged-ethernet-start': 2, 'untagged-ethernet-end': 2}]
        vlan._build_range_list = mock.Mock(return_value={'untagged-eth-list': untagged_eths})
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[2], untagged_trunks=[],
                           tagged_eths=[], tagged_trunks=[], veth=False, lif=None)

        ep = self.expected_payload
        ep['vlan']['untagged-eth-list'] = untagged_eths
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_untagged_trunks(self):
        untagged_trunks = [{'untagged-trunk-start': 2, 'untagged-trunk-end': 2}]
        vlan._build_range_list = mock.Mock(return_value={'untagged-trunk-list': untagged_trunks})
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[],
                           untagged_trunks=[2], tagged_eths=[],
                           tagged_trunks=[], veth=None, lif=None)

        ep = self.expected_payload
        ep['vlan']['untagged-trunk-list'] = untagged_trunks
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_tagged_eths(self):
        tagged_eths = [{'tagged-ethernet-start': 2, 'tagged-ethernet-end': 2}]
        vlan._build_range_list = mock.Mock(return_value={'tagged-eth-list': tagged_eths})
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[], untagged_trunks=[],
                           tagged_eths=[2], tagged_trunks=[], veth=False, lif=None)

        ep = self.expected_payload
        ep['vlan']['tagged-eth-list'] = tagged_eths
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_tagged_trunks(self):
        tagged_trunks = [{'tagged-trunk-start': 2, 'tagged-trunk-end': 2}]
        vlan._build_range_list = mock.Mock(return_value=tagged_trunks)
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[], untagged_trunks=[],
                           tagged_eths=[], tagged_trunks=[2], veth=False, lif=None)

        ep = self.expected_payload
        ep['vlan']['tagged-trunk-list'] = tagged_trunks
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_ve(self):
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[], untagged_trunks=[],
                           tagged_eths=[], tagged_trunks=[], veth=True, lif=None)

        ep = self.expected_payload
        ep['vlan']['ve'] = 1
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_create_lif(self):
        self.target.create(self.vlan_id, shared_vlan=False, untagged_eths=[], untagged_trunks=[],
                           tagged_eths=[], tagged_trunks=[], veth=False, lif=6)

        ep = self.expected_payload
        ep['vlan']['untagged-lif'] = 6
        self.client.http.request.assert_called_with("POST", self.url_prefix, ep, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=None)

    def test_vlan_delete(self):
        self.target.delete(self.vlan_id)
        self.client.http.request.assert_called_with(
            "DELETE", '{0}/{1}'.format(self.url_prefix, self.vlan_id), mock.ANY, mock.ANY,
            axapi_args=None, max_retries=None, timeout=None
        )
