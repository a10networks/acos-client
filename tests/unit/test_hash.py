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

import acos_client

servers = ['a', 'b', 'c', 'd', 'e', 'f']


class TestHash(unittest.TestCase):

    def test_hash(self):
        h = acos_client.Hash(servers)
        a = h.get_server('aaa')
        h.get_server('bbb')
        h.get_server('ccc')
        self.assertEqual(a, h.get_server('aaa'))
