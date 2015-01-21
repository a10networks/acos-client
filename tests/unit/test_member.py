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


class TestMember(unittest.TestCase):

    def test_member_delete(self):
        with mocks.MemberDelete().client() as c:
            c.slb.service_group.member.delete('pool1', 's1', 80)

    def test_member_delete_not_found(self):
        with mocks.MemberDeleteNotFound().client() as c:
            c.slb.service_group.member.delete('pool1', 's1', 80)

    def test_member_create(self):
        with mocks.MemberCreate().client() as c:
            c.slb.service_group.member.create('pool1', 's1', 80)

    def test_member_create_exists(self):
        with mocks.MemberCreateExists().client() as c:
            with self.assertRaises(acos_errors.Exists):
                c.slb.service_group.member.create('pool1', 's1', 80)

    def test_member_update(self):
        with mocks.MemberUpdate().client() as c:
            c.slb.service_group.member.update('pool1', 's1', 80,
                                              c.slb.DOWN)

    def test_member_update_not_found(self):
        with mocks.MemberUpdateNotFound().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.service_group.member.update(
                    'pool1', 's1', 80,
                    c.slb.DOWN)

    def test_member_update_no_such_service_group(self):
        with mocks.MemberUpdateNoSuchServiceGroup().client() as c:
            with self.assertRaises(acos_errors.NotFound):
                c.slb.service_group.member.update(
                    'pool1', 's1', 80,
                    c.slb.DOWN)
