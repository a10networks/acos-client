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

from acos_client.v30.base import BaseV30


class TestChildClass(BaseV30):
    def __init__(self, client):
        super(TestChildClass, self).__init__(client=client)
        self.url_prefix = "/url/prefix/"


class TestBaseV30Child(unittest.TestCase):

    def setUp(self) -> None:
        self.client = mock.MagicMock()
        self.child_cls = TestChildClass(client=self.client)
        self.url_prefix = "/url/prefix"

    def test_build_url(self):
        cases = [{
            "case_name": "arbitrary arguments",
            "args": ["first"],
            "kwargs": {},
            "expected": f"{self.url_prefix}/first"
        }, {
            "case_name": "arbitrary arguments and should end with separator",
            "args": ["first"],
            "kwargs": {"ends_with_separator": True},
            "expected": f"{self.url_prefix}/first/"
        }, {
            "case_name": "arbitrary arguments with empty string and None",
            "args": ["first", "", None, "second"],
            "kwargs": {},
            "expected": f"{self.url_prefix}/first/second"
        }, {
            "case_name": "arbitrary arguments and with slashes",
            "args": ["first", "/second/", "/third", "last"],
            "kwargs": {"ends_with_separator": True},
            "expected": f"{self.url_prefix}/first/second/third/last/"
        }, {
            "case_name": "arbitrary arguments and leading slash",
            "args": ["/suffix_with_leading_slash"],
            "kwargs": {},
            "expected": f"{self.url_prefix}/suffix_with_leading_slash"
        }, {
            "case_name": "keyword argument suffix with leading slash",
            "args": [],
            "kwargs": {"suffix": "/suffix_with_leading_slash"},
            "expected": f"{self.url_prefix}/suffix_with_leading_slash"
        }, {
            "case_name": "arbitrary and keyword arguments where only arbitrary args will be processed",
            "args": ["end", "result"],
            "kwargs": {"middle": "middle", "suffix": "suffix"},
            "expected": f"{self.url_prefix}/end/result"
        }, {
            "case_name": "keyword arguments suffix and middle",
            "args": [],
            "kwargs": {"middle": "middle", "suffix": "suffix"},
            "expected": f"{self.url_prefix}/middle/suffix"
        }, {
            "case_name": "keyword arguments suffix and middle with slashes",
            "args": [],
            "kwargs": {"middle": "/middle_with_slashes/", "suffix": "/suffix_with_slashes/"},
            "expected": f"{self.url_prefix}/middle_with_slashes/suffix_with_slashes"
        }, {
            "case_name": "keyword arguments suffix and middle with slashes",
            "args": [],
            "kwargs": {"middle": "/middle_with_slashes/", "suffix": "/suffix_with_slashes/", "ends_with_separator": True},
            "expected": f"{self.url_prefix}/middle_with_slashes/suffix_with_slashes/"
        }, {
            "case_name": "arbitrary arguments with slashes",
            "args": ["/first_with_slashes/", "/second_with_slashes/"],
            "kwargs": {},
            "expected": f"{self.url_prefix}/first_with_slashes/second_with_slashes"
        }, {
            "case_name": "arbitrary arguments with slashes should end with separator",
            "args": ["/first/with/slashes/", "/second/with/slashes/"],
            "kwargs": {"ends_with_separator": True},
            "expected": f"{self.url_prefix}/first/with/slashes/second/with/slashes/"
        }, {
            "case_name": "keyword arguments with slashes",
            "args": [],
            "kwargs": {"middle": "middle/with/slash", "suffix": "suffix/with/slash/"},
            "expected": f"{self.url_prefix}/middle/with/slash/suffix/with/slash"
        }, {
            "case_name": "keyword arguments with slashes should end with separator",
            "args": [],
            "kwargs": {"middle": "middle/with/slash", "suffix": "suffix/with/slash/", "ends_with_separator": True},
            "expected": f"{self.url_prefix}/middle/with/slash/suffix/with/slash/"
        }]
        for case in cases:
            expected_url = case["expected"]
            actual_url = self.child_cls._build_url(*case["args"], **case["kwargs"])
            self.assertEqual(expected_url, actual_url)

    def test_convert_to_int(self):
        cases = [
            {"param": 1, "expected_return": 0, "case_name": "int 1 is passed"},
            {"param": 0, "expected_return": 0, "case_name": "int 0 is passed"},
            {"param": True, "expected_return": 1, "case_name": "True is passed"},
            {"param": False, "expected_return": 0, "case_name": "False is passed"},
            {"param": "str_value", "expected_return": 0, "case_name": "string is passed"},
            {"param": "", "expected_return": 0, "case_name": "empty string is passed"},
            {"param": None, "expected_return": 0, "case_name": "None is passed"},
            {"param": [], "expected_return": 0, "case_name": "empty list is passed"},
            {"param": {}, "expected_return": 0, "case_name": "empty dict is passed"},
        ]
        for case in cases:
            ret_val = BaseV30.convert_to_int(case["param"])
            self.assertIs(case["expected_return"], ret_val)
