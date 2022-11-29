# Copyright (C) 2022, A10 Networks Inc. All rights reserved.
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

from acos_client.v30.class_list import ClassList

class TestClassList(unittest.TestCase):

    def setUp(self) -> None:
        self.client = mock.MagicMock()
        self.class_list = ClassList(client=self.client)
        self.url_prefix = "/axapi/v3/class-list"
        self.name = "class_list_name"

    def test_class_list_get_list(self):
        self.class_list.get_list()
        _url = f"{self.url_prefix}"
        self.client.http.request.assert_called_with(
            "GET", _url, {}, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )
        self.class_list.get_all()
        self.client.http.request.assert_called_with(
            "GET", _url, {}, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )
        self.class_list.all()
        self.client.http.request.assert_called_with(
            "GET", _url, {}, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_get(self):
        _url = f"{self.url_prefix}/{self.name}"
        self.class_list.get(self.name)
        self.client.http.request.assert_called_with(
            "GET", _url, {}, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_create(self):
        _url = f"{self.url_prefix}"
        self.class_list.create(self.name, ipv4addr="192.168.1.1/32", lsn_lid=5, ipv6_addr="fe80::1/64", v6_lsn_lid=2)
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 0,
                "ipv4-list": [{"ipv4addr": "192.168.1.1/32", "lsn-lid": 5}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_create_without_lsn_lid(self):
        _url = f"{self.url_prefix}"
        self.class_list.create(self.name, ipv4addr="192.168.1.1/32")
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 0,
                "ipv4-list": [{"ipv4addr": "192.168.1.1/32"}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_create_v6(self):
        _url = f"{self.url_prefix}"
        self.class_list.create(self.name, ipv6_addr="fe80::1/64", v6_lsn_lid=2)
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 0,
                "ipv6-list": [{"ipv6-addr": "fe80::1/64", "v6-lsn-lid": 2}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_create_v6_without_lsn_lid(self):
        _url = f"{self.url_prefix}"
        self.class_list.create(self.name, ipv6_addr="fe80::1/64")
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 0,
                "ipv6-list": [{"ipv6-addr": "fe80::1/64"}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_update(self):
        _url = f"{self.url_prefix}/{self.name}"
        self.class_list.update(self.name, file=True, ipv4addr="192.168.1.0/28", lsn_lid=10)
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 1,
                "ipv4-list": [{"ipv4addr": "192.168.1.0/28", "lsn-lid": 10}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_update_v6(self):
        _url = f"{self.url_prefix}"
        self.class_list.create(self.name, ipv6_addr="fe80::1/128", v6_lsn_lid=10)
        expected_payload = {
            "class-list" : {
                "name": self.name,
                "file": 0,
                "ipv6-list": [{"ipv6-addr": "fe80::1/128", "v6-lsn-lid": 10}],
            }
        }
        self.client.http.request.assert_called_with(
            "POST", _url, expected_payload, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )

    def test_class_list_delete(self):
        _url = f"{self.url_prefix}/{self.name}"
        self.class_list.delete(self.name)
        self.client.http.request.assert_called_with(
            "DELETE", _url, {}, mock.ANY, axapi_args=None, max_retries=None, timeout=mock.ANY,
        )
