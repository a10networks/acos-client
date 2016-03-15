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


class TestServiceGroup(unittest.TestCase):

    def test_sg_delete(self):
        with mocks.ServiceGroupDelete().client() as c:
            c.slb.service_group.delete('pool1')

    def test_sg_delete_not_found(self):
        with mocks.ServiceGroupDeleteNotFound().client() as c:
            c.slb.service_group.delete('pool1')

    def test_sg_create(self):
        with mocks.ServiceGroupCreate().client() as c:
            c.slb.service_group.create('pool1')

    def test_sg_create_exists(self):
        with mocks.ServiceGroupCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.service_group.create('pool1')

    def test_sg_update(self):
        with mocks.ServiceGroupUpdate().client() as c:
            c.slb.service_group.update(
                'pool1',
                lb_method=c.slb.service_group.LEAST_CONNECTION)

    def test_sg_update_not_found(self):
        with mocks.ServiceGroupUpdateNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.service_group.update(
                    'pool1',
                    lb_method=c.slb.service_group.LEAST_CONNECTION)

    def test_sg_search(self):
        with mocks.ServiceGroupSearch().client() as c:
            c.slb.service_group.get('pool1')

    def test_sg_search_not_found(self):
        with mocks.ServiceGroupSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.service_group.get('pool1')
