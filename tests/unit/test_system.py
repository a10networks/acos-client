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
import v21_mocks as mocks


class TestSystem(unittest.TestCase):

    def test_information(self):
        m = mocks.SystemInformation()
        with m.client() as c:
            r = c.system.information()
            self.assertIn('system_information', r)

    def test_write_memory(self):
        m = mocks.SystemWriteMemory()
        with m.client() as c:
            c.system.action.write_memory()
