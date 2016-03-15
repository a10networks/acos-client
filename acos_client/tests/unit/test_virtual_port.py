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


class TestVirtualPort(unittest.TestCase):

    def test_virtual_port_delete(self):
        with mocks.VirtualPortDelete().client() as c:
            c.slb.virtual_server.vport.delete('vip1', 'vip1_VPORT',
                                              c.slb.virtual_server.vport.HTTP,
                                              '80')

    def test_virtual_port_delete_not_found(self):
        with mocks.VirtualPortDeleteNotFound().client() as c:
            c.slb.virtual_server.vport.delete('vip1', 'vip1_VPORT',
                                              c.slb.virtual_server.vport.HTTP,
                                              '80')

    def test_virtual_port_create(self):
        with mocks.VirtualPortCreate().client() as c:
            c.slb.virtual_server.vport.create(
                'vip1', 'vip1_VPORT',
                protocol=c.slb.virtual_server.vport.HTTP,
                port='80',
                service_group_name='pool1')

    def test_virtual_port_create_exists(self):
        with mocks.VirtualPortCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.virtual_server.vport.create(
                    'vip1', 'vip1_VPORT',
                    protocol=c.slb.virtual_server.vport.HTTP,
                    port='80',
                    service_group_name='pool1')
