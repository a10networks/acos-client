# Copyright 2016, All Rights Reserved,  A10 Networks.
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

import mock
import unittest2

from acos_client import logutils as target


class TestLogutils(unittest2.TestCase):
    def setUp(self):
        self.clean_fields = ["username", "password"]

        self.obj_flat = self._fakeobj(a=1, b=2, username="admin", password="secret")
        self.obj_onelevel = self._fakeobj(a=1,
                                          b=2,
                                          credentials=self._fakeobj(
                                              username="admin",
                                              password="secret"))
        self.obj_twolevel = self._fakeobj(a=1,
                                          b=2,
                                          credentials=self._fakeobj(
                                              inside_secret=self._fakeobj(
                                                  username="admin",
                                                  password="secret")))
        self.flat_dict = {
            "a": 1,
            "b": 2,
            "username": "admin",
            "password": "secret"
        }

        self.dict_onelevel = {
            "a": 1,
            "b": 2,
            "credentials": {
                "username": "admin",
                "password": "secret"
            }
        }

        self.dict_twolevel = {
            "a": 1,
            "b": 2,
            "credentials": {
                "inside_secret": {
                    "username": "admin",
                    "password": "secret"
                }
            }
        }

    def _fakeobj(self, *args, **kwargs):
        return FakeObject(**kwargs)

    def test_clean_flat_dict(self):
        actual = target.clean(self.flat_dict)
        self.assertEqual(target.REPLACEMENT, actual["username"])
        self.assertEqual(target.REPLACEMENT, actual["password"])
        self.assertEqual(self.flat_dict["a"], actual["a"])

    def test_clean_onelevel_dict(self):
        actual = target.clean(self.dict_onelevel).get("credentials")

        self.assertEqual(target.REPLACEMENT, actual["username"])
        self.assertEqual(target.REPLACEMENT, actual["password"])
        self.assertEqual(1, self.dict_onelevel["a"])

    def test_clean_twolevel_dict(self):
        actual = target.clean(self.dict_twolevel).get("credentials").get("inside_secret")

        self.assertEqual(target.REPLACEMENT, actual["username"])
        self.assertEqual(target.REPLACEMENT, actual["password"])

    def test_obj_flat(self):
        actual = target.clean(self.obj_flat)
        self.assertEqual(target.REPLACEMENT, actual.username)
        self.assertEqual(target.REPLACEMENT, actual.password)

    def test_obj_onelevel(self):
        actual = target.clean(self.obj_onelevel).credentials
        self.assertEqual(target.REPLACEMENT, actual.username)
        self.assertEqual(target.REPLACEMENT, actual.password)

    def test_obj_twolevel(self):
        actual = target.clean(self.obj_twolevel).credentials.inside_secret
        self.assertEqual(target.REPLACEMENT, actual.username)
        self.assertEqual(target.REPLACEMENT, actual.password)

    def test_tuple_dict(self):
        actual = target.clean(
            (1, {'credentials': {
                'username': 'admin',
                'password': 'secret'}
            }))
        expected = (1, {'credentials': {
            'username': target.REPLACEMENT,
            'password': target.REPLACEMENT}
            })
        self.assertEqual(expected, actual)

    def test_list_dict(self):
        actual = target.clean(
            [{'credentials': {
                'username': 'admin',
                'password': 'secret'}}])
        expected = [{'credentials': {
            'username': target.REPLACEMENT,
            'password': target.REPLACEMENT}
            }]
        self.assertEqual(expected, actual)

    def test_mock(self):
        # It's likely that clean will be called with a mock during testing.
        # It shouldn't blow up

        m = mock.MagicMock()
        str(m)
        target.clean(m)


class FakeObject(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
