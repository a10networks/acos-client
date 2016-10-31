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


class TestServer(unittest.TestCase):

    def test_server_delete(self):
        with mocks.ServerDelete().client() as c:
            c.slb.server.delete('s1')

    def test_server_delete_not_found(self):
        with mocks.ServerDeleteNotFound().client() as c:
            c.slb.server.delete('s1')

    def test_server_create(self):
        with mocks.ServerCreate().client() as c:
            c.slb.server.create('s1', '192.168.2.254', 1337)

    def test_server_create_exists(self):
        with mocks.ServerCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.server.create('s1', '192.168.2.254', 1337)

    def test_server_search(self):
        with mocks.ServerSearch().client() as c:
            c.slb.server.get('s1')

    def test_server_search_not_found(self):
        with mocks.ServerSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.server.get('s1')
