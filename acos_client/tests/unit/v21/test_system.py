# Copyright 2014,  Doug Wiegley,  A10 Networks.
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
    import unittest2 as unittest
except ImportError:
    import unittest

from acos_client import client
import responses


HOSTNAME = 'fake_a10'
BASE_URL = "https://{}:443/services/rest/v2.1/?format=json&method=".format(HOSTNAME)
AUTH_URL = "{}authenticate".format(BASE_URL)
SYS_INFO_URL = '{}system.information.get&session_id={}'.format(BASE_URL, 'foobar')
SYS_WRITE_MEM_URL = '{}system.action.write_memory&session_id={}'.format(BASE_URL, 'foobar')


class TestHighAvailability(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '21', 'fake_username', 'fake_password')

    @responses.activate
    def test_system_information(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            'system_information': {
                'advanced_core_os_on_compact_flash1': 'No Software',
                'advanced_core_os_on_compact_flash2': 'No Software',
                'advanced_core_os_on_harddisk1': '2.7.1-P3-AWS(build: 4)',
                'advanced_core_os_on_harddisk2': '2.7.1-P3-AWS(build: 4)',
                'aflex_engine_version': '2.0.0',
                'axapi_version': '2.1',
                'current_time': '03:25:47 IST Tue Jul 1 2014',
                'firmware_version': 'N/A',
                'last_config_saved': '06:25:26 GMT Sat Dec 28 2013',
                'serial_number': 'N/A',
                'software_version': '2.7.1-P3-AWS(build: 4)',
                'startup_mode': 'hard disk primary',
                'technical_support': 'www.a10networks.com/support '
            }
        }
        responses.add(responses.GET, SYS_INFO_URL, json=json_response, status=200)

        resp = self.client.system.information()

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, SYS_INFO_URL)

    @responses.activate
    def test_system_write_memory(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {'response': {'status': 'OK'}}
        responses.add(responses.GET, SYS_WRITE_MEM_URL, json=json_response, status=200)

        resp = self.client.system.action.write_memory()

        self.assertIsNone(resp)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, SYS_WRITE_MEM_URL)
