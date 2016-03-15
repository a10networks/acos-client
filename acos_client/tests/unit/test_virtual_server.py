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


class TestVirtualServer(unittest.TestCase):

    def test_virtual_server_delete(self):
        with mocks.VirtualServerDelete().client() as c:
            c.slb.virtual_server.delete('vip1')

    def test_virtual_server_delete_not_found(self):
        with mocks.VirtualServerDeleteNotFound().client() as c:
            c.slb.virtual_server.delete('vip1')

    def test_virtual_server_create(self):
        with mocks.VirtualServerCreate().client() as c:
            c.slb.virtual_server.create('vip1', '192.168.2.250')

    def test_virtual_server_create_exists(self):
        with mocks.VirtualServerCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.virtual_server.create('vip1', '192.168.2.250')

    def test_virtual_server_search(self):
        with mocks.VirtualServerSearch().client() as c:
            c.slb.virtual_server.get('vip1')

    def test_virtual_server_search_not_found(self):
        with mocks.VirtualServerSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.virtual_server.get('vip1')
