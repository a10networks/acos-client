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

import mock
import unittest2 as unittest

from acos_client.v30.slb import service_group


class TestServiceGroup(unittest.TestCase):

    def test_sg_update_health_check_disable(self):
        client = mock.MagicMock()
        sg = service_group.ServiceGroup(client)

        sg.update('fake-pool-name', health_monitor="", health_check_disable=True)

        expected = {
            'service-group': {
                'name': 'fake-pool-name',
                'health-check-disable': 1
            }
        }

        ((method, url, params, header), kwargs) = client.http.request.call_args

        self.assertEqual(expected, params)

    def test_sg_update_health_check(self):
        client = mock.MagicMock()
        sg = service_group.ServiceGroup(client)

        sg.update('fake-pool-name', health_monitor="fake-hm")

        expected = {
            'service-group': {
                'name': 'fake-pool-name',
                'health-check': 'fake-hm'
            }
        }

        ((method, url, params, header), kwargs) = client.http.request.call_args

        self.assertEqual(expected, params)

    def test_stats(self):
        client = mock.MagicMock()
        sg = service_group.ServiceGroup(client)
        sgname = "fake-pool"
        sg.stats(sgname)

        ((method, url, params, header), kwargs) = client.http.request.call_args
        expected_url = "/axapi/v3/slb/service-group/{0}/stats".format(sgname)
        self.assertEqual(method, "GET")
        self.assertEqual(expected_url, url)
