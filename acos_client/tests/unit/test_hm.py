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

import unittest2 as unittest

import acos_client.errors as acos_errors

import v21_mocks as mocks


class TestHealthMonitor(unittest.TestCase):

    def test_hm_delete(self):
        with mocks.HealthMonitorDelete().client() as c:
            c.slb.hm.delete('hm1')

    def test_hm_delete_not_found(self):
        with mocks.HealthMonitorDeleteNotFound().client() as c:
            c.slb.hm.delete('hm1')

    def test_hm_create(self):
        with mocks.HealthMonitorCreate().client() as c:
            c.slb.hm.create('hm1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

    def test_hm_create_exists(self):
        with mocks.HealthMonitorCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.hm.create('hm1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

    def test_hm_update(self):
        with mocks.HealthMonitorUpdate().client() as c:
            c.slb.hm.update('hm1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

    def test_hm_update_not_found(self):
        with mocks.HealthMonitorUpdateNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.hm.update('hm1', 'HTTP', 5, 5, 5, 'GET', '/', '200', 80)

    def test_hm_search(self):
        with mocks.HealthMonitorSearch().client() as c:
            c.slb.hm.get('hm1')

    def test_hm_search_not_found(self):
        with mocks.HealthMonitorSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.hm.get('hm1')
