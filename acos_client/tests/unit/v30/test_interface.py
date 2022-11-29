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

from acos_client.v30 import interface


class TestInterface(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = interface.Interface(self.client)
        self.url_prefix = "/axapi/v3/interface/"

    def test_interface_get_list(self):
        self.target.get_list()
        self.client.http.request.assert_called_with("GET", self.url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_interface_get(self):
        self.target.get()
        self.client.http.request.assert_called_with("GET", self.url_prefix, {}, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def _test_interface_create_dhcp(self, dhcp=True):
        expected = 1 if dhcp else 0
        ifnum = 1
        expected_payload = {self.target.iftype: {'ip': {'dhcp': expected}, 'ifnum': ifnum}}
        self.target.create(ifnum, dhcp=dhcp)
        self.client.http.request.assert_called_with("POST", self.url_prefix,  # URL + ifnum expected
                                                    expected_payload, mock.ANY, axapi_args=None,
                                                    max_retries=None, timeout=mock.ANY)

    def test_interface_create_dhcp_negative(self):
        self._test_interface_create_dhcp(False)

    def test_interface_create_dhcp_positive(self):
        self._test_interface_create_dhcp()

    def test_interface_create_ipaddress(self):
        ifnum = 1
        ip_address = "128.0.0.1"
        ip_netmask = "255.255.255.0"
        self.target.create(ifnum, dhcp=False, ip_address=ip_address, ip_netmask=ip_netmask)
        self.client.http.request.assert_called_with("POST", self.url_prefix, mock.ANY, mock.ANY,
                                                    axapi_args=None, max_retries=None, timeout=mock.ANY)

    def test_interface_delete(self):
        ifnum = 1
        self.target.delete(1)
        self.client.http.request.assert_called_with("DELETE", self.url_prefix + str(ifnum),
                                                    mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                    timeout=mock.ANY)

    def test_interface_update(self):
        ifnum = 1
        ip_address = "128.0.0.1"
        ip_netmask = "255.255.255.0"

        self.target.update(ifnum, dhcp=False, ip_address=ip_address, ip_netmask=ip_netmask)

        self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                    mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                    timeout=mock.ANY)

    def test_interface_enable_positive(self):
        ifnum = 1
        ip_address = "128.0.0.1"
        ip_netmask = "255.255.255.0"

        self.target.update(ifnum, dhcp=False, ip_address=ip_address, ip_netmask=ip_netmask,
                           enable=True)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertEqual("enable", params[self.target.iftype]["action"])

        self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                    mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                    timeout=mock.ANY)

    def test_interface_enable_negative(self):
        ifnum = 1
        ip_address = "128.0.0.1"
        ip_netmask = "255.255.255.0"

        self.target.update(ifnum, dhcp=False, ip_address=ip_address, ip_netmask=ip_netmask,
                           enable=False)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual("disable", params[self.target.iftype]["action"])

        self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                    mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                    timeout=mock.ANY)


class TestEthernetInterface(TestInterface):
        def setUp(self):
            super(TestEthernetInterface, self).setUp()
            self.target = interface.EthernetInterface(self.client)
            self.url_prefix = "{0}{1}/".format(self.url_prefix, self.target.iftype)


class TestManagementInterface(TestInterface):
        def setUp(self):
            super(TestManagementInterface, self).setUp()
            self.target = interface.ManagementInterface(self.client)
            self.url_prefix = "{0}{1}/".format(self.url_prefix, self.target.iftype)

class TestVirtualEthernetInterface(TestInterface):

        def setUp(self):
            super(TestVirtualEthernetInterface, self).setUp()
            self.target = interface.VirtualEthernet(self.client)
            self.url_prefix = f"{self.url_prefix}{self.target.iftype}/"

        def test_interface_create_ipaddress(self):
            ifnum = 33
            ipv4_address = [("192.168.254.1", "255.255.255.252")]
            expected_payload = {'ve': {'ifnum': 33, 'ip': {'address-list': [{'ipv4-address': '192.168.254.1', 'ipv4-netmask': '255.255.255.252'}]}}}
            self.target.create(ifnum, ipv4_address=ipv4_address)
            self.client.http.request.assert_called_with("POST", self.url_prefix, expected_payload, mock.ANY,
                                                        axapi_args=None, max_retries=None, timeout=mock.ANY)

        def test_interface_update(self):
            ifnum = 33
            ipv6_address = ['fe80::1/64']
            expected_payload = {'ve': {'ifnum': 33, 'ipv6': {'address-list': [{'ipv6-addr': 'fe80::1/64'}]}}}
            self.target.update(ifnum, ipv6_address=ipv6_address)
            self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                        expected_payload, mock.ANY, axapi_args=None, max_retries=None,
                                                        timeout=mock.ANY)

        def test_interface_enable_positive(self):
            ifnum = 1
            self.target.update(ifnum, enable=True)
            ((method, url, params, header), kwargs) = self.client.http.request.call_args
            self.assertEqual("enable", params[self.target.iftype]["action"])
            self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                        mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                        timeout=mock.ANY)

        def test_interface_enable_negative(self):
            ifnum = 1
            self.target.update(ifnum, enable=False)
            ((method, url, params, header), kwargs) = self.client.http.request.call_args
            self.assertEqual("disable", params[self.target.iftype]["action"])
            self.client.http.request.assert_called_with("POST", self.url_prefix + str(ifnum),
                                                        mock.ANY, mock.ANY, axapi_args=None, max_retries=None,
                                                        timeout=mock.ANY)

