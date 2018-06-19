# Copyright 2018,  A10 Networks.
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

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest


def test_suite():
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("acos_client.tests")
    return test_suite
