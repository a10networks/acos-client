# Copyright 2014-2016,  A10 Networks.
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

from acos_client.v30.slb import common


class TestSFlow(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = common.SLBCommon(self.client)

    def test_underscore_to_dash(self):
        expected = "no-dsr-health-check"
        actual = self.target._underscore_to_dash(expected)
        self.assertEqual(expected.replace('_', '-'), actual)

    def test_create(self):
        in_params = {"no_dsr_health_check": 1, "nounderscores": "string", "boolean": False}
        expected_params = {"no-dsr-health-check": 1, "nounderscores": "string", "boolean": False}
        self.target.create(**in_params)
        ((method, url, params, header), kwargs) = self.client.http.request.call_args
        self.assertTrue('GET', method)
        self.assertTrue('/axapi/v3/' + self.target.url_prefix, url)
        self.assertTrue(expected_params, params)
