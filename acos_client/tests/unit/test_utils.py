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

import acos_client


class TestUtils(unittest.TestCase):

    def test_version(self):
        exp = (4, 1, 1, 0, 0, 0)
        tup = acos_client.utils.acos_version("4.1.1")
        self.assertEqual(tup, exp)

        exp = (4, 1, 1, 0, 2, 0)
        tup = acos_client.utils.acos_version("4.1.1-P2")
        self.assertEqual(tup, exp)

        exp = (4, 1, 1, 0, 2, 0)
        tup = acos_client.utils.acos_version("4.1.1-p2")
        self.assertEqual(tup, exp)

        exp = (4, 1, 4, 1, 2, 0)
        tup = acos_client.utils.acos_version("4.1.4-GR1-P2")
        self.assertEqual(tup, exp)

        exp = (4, 1, 4, 1, 3, 4)
        tup = acos_client.utils.acos_version("4.1.4-gr1-p3-sp4")
        self.assertEqual(tup, exp)

        exp = (4, 1, 4, 1, 3, 4)
        tup = acos_client.utils.acos_version("4.1.4-GR1-P3-SP4")
        self.assertEqual(tup, exp)

        exp = (5, 2, 0, 0, 0, 0)
        tup = acos_client.utils.acos_version("5.2.0")
        self.assertEqual(tup, exp)

    def test_version_cmp(self):
        rt = acos_client.utils.acos_version_cmp("5.2.0", "4.2.0")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.3.0", "5.2.0")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.0", "5.2.0")
        self.assertEqual(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.1", "5.2.0")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.1-P1", "5.2.1")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.1-GR1-P1", "5.2.1-GR1")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.1-GR1-P3-SP1", "5.2.1-GR1-P3")
        self.assertGreater(rt, 0)

        # case insensitive
        rt = acos_client.utils.acos_version_cmp("5.2.1-GR1-p1", "5.2.1-GR1")
        self.assertGreater(rt, 0)

        rt = acos_client.utils.acos_version_cmp("5.2.1-GR1-P3-SP1", "5.2.1-gr1-p3-sp1")
        self.assertEqual(rt, 0)
