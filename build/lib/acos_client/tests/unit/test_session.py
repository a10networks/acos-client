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

import acos_client


class TestSession(unittest.TestCase):

    def test_id(self):
        s = mocks.Session({'username': 'mongo', 'password': 'teddybear',
                           'session_id': 'fruitloops'})
        with s.client() as c:
            self.assertEqual(c.session.session_id, None)
            self.assertEqual(c.session.id, 'fruitloops')
            self.assertEqual(c.session.session_id, 'fruitloops')

    def test_authenticate(self):
        s = mocks.Session({'username': 'panda', 'password': 'weak'})
        with s.client() as c:
            r = c.session.authenticate('panda', 'weak')
            self.assertNotEqual(r['session_id'], None)

    def test_bad_authenticate(self):
        s = mocks.SessionBadPassword({'username': 'user', 'password': 'pass'})
        with s.client() as c:
            self.assertEqual(c.session.session_id, None)
            try:
                c.session.authenticate('user', 'pass')
            except acos_client.errors.AuthenticationFailure:
                pass
            self.assertEqual(c.session.session_id, None)

    def test_close(self):
        m = mocks.Close()
        with m.client() as c:
            c.session.close()
            self.assertEqual(c.session.session_id, None)

    def test_close_with_bad_session_id(self):
        m = mocks.CloseBadSession({'session_id': 'badsessionid'})
        with m.client() as c:
            c.session.close()
            self.assertEqual(c.session.session_id, None)
