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


class TestHttpCookiePersistence(unittest.TestCase):

    def test_http_cookie_delete(self):
        with mocks.HttpCookiePersistenceDelete().client() as c:
            c.slb.template.cookie_persistence.delete('cp1')

    def test_http_cookie_delete_not_found(self):
        with mocks.HttpCookiePersistenceDeleteNotFound().client() as c:
            c.slb.template.cookie_persistence.delete('cp1')

    def test_http_cookie_create(self):
        with mocks.HttpCookiePersistenceCreate().client() as c:
            c.slb.template.cookie_persistence.create('cp1')

    def test_http_cookie_create_exists(self):
        with mocks.HttpCookiePersistenceCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.template.cookie_persistence.create('cp1')

    def test_http_cookie_search(self):
        with mocks.HttpCookiePersistenceSearch().client() as c:
            c.slb.template.cookie_persistence.get('cp1')

    def test_http_cookie_search_not_found(self):
        with mocks.HttpCookiePersistenceSearchNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.template.cookie_persistence.get('cp1')
