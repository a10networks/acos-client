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


class TestPartition(unittest.TestCase):

    # Test harness bug with delete
    # def test_partition_delete(self):
    #     with mocks.PartitionDelete().client() as c:
    #         c.system.partition.delete('p1')

    # def test_partition_delete_not_found(self):
    #     with mocks.PartitionDeleteNotFound().client() as c:
    #         c.system.partition.delete('p1')

    def test_partition_create(self):
        with mocks.PartitionCreate().client() as c:
            c.system.partition.create('p1')

    def test_partition_create_exists(self):
        with mocks.PartitionCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.system.partition.create('p1')

    def test_partition_exists(self):
        with mocks.PartitionExists().client() as c:
            self.assertTrue(c.system.partition.exists('p1'))

    def test_partition_exists_not_found(self):
        with mocks.PartitionExistsNotFound().client() as c:
            self.assertFalse(c.system.partition.exists('p1'))

    def test_partition_active(self):
        with mocks.PartitionActive().client() as c:
            c.system.partition.active('p1')

    def test_partition_active_not_found(self):
        with mocks.PartitionActiveNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.system.partition.active('p1')
