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

from acos_client import errors as acos_errors
from acos_client.v30.slb import member


class TestMember(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.member = member.Member(self.client)
        self.member._get = mock.MagicMock(side_effect=acos_errors.NotFound)

        # common test parameter(s) throughout all test-cases
        self._sg_name = 'fake-sg'

    def test_create_enable_member(self):
        expected = {
            'member': {
                'name': 'fake-srever',
                'port': 80,
                'member-stats-data-disable': self.member.STATUS_ENABLE,
                'member-state': 'enable',
            }
        }
        self.member.create(self._sg_name, 'fake-srever', 80)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(url, '/axapi/v3/slb/service-group/%s/member/' % (self._sg_name))
        self.assertEqual(params, expected)

    def test_create_disable_member(self):
        expected = {
            'member': {
                'name': 'fake-srever',
                'port': 80,
                'member-stats-data-disable': self.member.STATUS_DISABLE,
                'member-state': 'disable',
            }
        }
        self.member.create(self._sg_name, 'fake-srever', 80, self.member.STATUS_DISABLE, False)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(params, expected)

    def test_update_enable_member(self):
        expected = {
            'member': {
                'name': 'fake-srever',
                'port': 443,
                'member-stats-data-disable': self.member.STATUS_ENABLE,
                'member-state': 'enable',
            }
        }
        self.member.update(self._sg_name, 'fake-srever', 443)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(url, '/axapi/v3/slb/service-group/%s/member/%s+%s/' %
                              (self._sg_name,
                               expected['member']['name'],
                               expected['member']['port']))
        self.assertEqual(params, expected)

    def test_update_disable_member(self):
        expected = {
            'member': {
                'name': 'fake-srever',
                'port': 443,
                'member-stats-data-disable': self.member.STATUS_DISABLE,
                'member-state': 'disable',
            }
        }
        self.member.update(self._sg_name, 'fake-srever', 443, self.member.STATUS_DISABLE, False)

        ((method, url, params, header), kwargs) = self.client.http.request.call_args

        self.assertEqual(url, '/axapi/v3/slb/service-group/%s/member/%s+%s/' %
                              (self._sg_name,
                               expected['member']['name'],
                               expected['member']['port']))
        self.assertEqual(params, expected)
