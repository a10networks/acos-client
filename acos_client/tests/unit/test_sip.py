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


class TestSourceIpPersistence(unittest.TestCase):

    def test_source_ip_pers_delete(self):
        with mocks.SourceIpPersistenceDelete().client() as c:
            c.slb.template.src_ip_persistence.delete('sip1')

    def test_source_ip_pers_delete_not_found(self):
        with mocks.SourceIpPersistenceDeleteNotFound().client() as c:
            c.slb.template.src_ip_persistence.delete('sip1')

    def test_source_ip_pers_create(self):
        with mocks.SourceIpPersistenceCreate().client() as c:
            c.slb.template.src_ip_persistence.create('sip1')

    def test_source_ip_pers_create_exists(self):
        with mocks.SourceIpPersistenceCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.template.src_ip_persistence.create('sip1')

    def test_source_ip_pers_search(self):
        with mocks.SourceIpPersistenceSearch().client() as c:
            c.slb.template.src_ip_persistence.get('sip1')

    def test_source_ip_pers_search_not_found(self):
        with mocks.SourceIpPersistenceSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.template.src_ip_persistence.get('sip1')
