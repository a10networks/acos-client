# Copyright 2022, A10 Networks
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

from acos_client import errors as acos_errors
from acos_client.v30 import base


class ClassList(base.BaseV30):

    @property
    def url_prefix(self):
        return "/class-list"

    def create(self, name, file=False, ipv4addr=None, lsn_lid=None, ipv6_addr=None, v6_lsn_lid=None):
        """
        Create class-list into the device.
        :param name: name of the class-list going to be created
        :param file: Create/Edit a class-list stored as a file. default 0 and if True 1 else 0
        :param ipv4addr: ipv4 address for ipv4-list
        :param lsn_lid: LSN limit ID for ipv4-list
        :param ipv6_addr: ipv6 address for ipv6-list
        :param v6_lsn_lid: LSN limit ID for ipv6-list
        :raise `acos_errors.Exists` when the object exists and no need to create.
        """
        payload = self._build_payload(
            name=name, file=file, ipv4addr=ipv4addr, lsn_lid=lsn_lid, ipv6_addr=ipv6_addr, v6_lsn_lid=v6_lsn_lid
        )

        return self._post(self._build_url(), payload)

    def get(self, name):
        """
        Get class-list config by name.
        :param name: name of the class-list configured on the device.
        :raise `acos_errors.NotFound` when the object does not exist and cannot be retrieved.
        """
        return self._get(self._build_url(suffix=name))

    def delete(self, name):
        """
        Delete class-list config by name.
        :param name: name of the class-list configured on the device.
        """
        return self._delete(self._build_url(suffix=name))

    def replace(self, name, file=False, ipv4addr=None, lsn_lid=None, ipv6_addr=None, v6_lsn_lid=None):
        """
        Replace class-list with the given `name`. ipv4 and ipv6 addresses are mutually exclusive because
        class-list type is determined according to ipv4-list or ipv6-list existence on device configuration.

        :param name: name of the class-list going to be created
        :param file: Create/Edit a class-list stored as a file. default 0 and if True 1 else 0
        :param ipv4addr: ipv4 address for ipv4-list
        :param lsn_lid: LSN limit ID for ipv4-list
        :param ipv6_addr: ipv6 address for ipv6-list
        :param v6_lsn_lid: LSN limit ID for ipv6-list
        :raise `acos_errors.NotFound` when the object does not exist and cannot be updated.
        """
        payload = self._build_payload(
            name=name, file=file, ipv4addr=ipv4addr, lsn_lid=lsn_lid, ipv6_addr=ipv6_addr, v6_lsn_lid=v6_lsn_lid
        )

        return self._put(self._build_url(suffix=name), payload)

    def update(self, name, file=False, ipv4addr=None, lsn_lid=None, ipv6_addr=None, v6_lsn_lid=None):
        """
        Update class-list with the given `name`. ipv4 and ipv6 addresses are mutually exclusive because
        class-list type is determined according to ipv4-list or ipv6-list existence on device configuration.

        :param name: name of the class-list going to be created
        :param file: Create/Edit a class-list stored as a file. default 0 and if True 1 else 0
        :param ipv4addr: ipv4 address for ipv4-list
        :param lsn_lid: LSN limit ID for ipv4-list
        :param ipv6_addr: ipv6 address for ipv6-list
        :param v6_lsn_lid: LSN limit ID for ipv6-list
        :raise `acos_errors.NotFound` when the object does not exist and cannot be updated.
        """
        payload = self._build_payload(
            name=name, file=file, ipv4addr=ipv4addr, lsn_lid=lsn_lid, ipv6_addr=ipv6_addr, v6_lsn_lid=v6_lsn_lid
        )

        return self._post(self._build_url(suffix=name), payload)

    def create_or_update(self, name, file=False, ipv4addr=None, lsn_lid=None, ipv6_addr=None, v6_lsn_lid=None):
        """
        `self.create` method raises `acos_errors.Exists` when the object exists, so nothing need to create.
        `self.update` method raises `acos_errors.NotFound` when the object does not found, so nothing needs to be updated.
        In contrary, this method does not raise any exception. If object exists, it updates config else create it.

        :param name: name of the class-list going to be created
        :param file: Create/Edit a class-list stored as a file. default 0 and if True 1 else 0
        :param ipv4addr: ipv4 address for ipv4-list
        :param lsn_lid: LSN limit ID for ipv4-list
        :param ipv6_addr: ipv6 address for ipv6-list
        :param v6_lsn_lid: LSN limit ID for ipv6-list
        """
        if self.exists(name):
            return self.update(
                name=name, file=file, ipv4addr=ipv4addr, lsn_lid=lsn_lid, ipv6_addr=ipv6_addr, v6_lsn_lid=v6_lsn_lid
            )
        else:
            return self.create(
                name=name, file=file, ipv4addr=ipv4addr, lsn_lid=lsn_lid, ipv6_addr=ipv6_addr, v6_lsn_lid=v6_lsn_lid
            )

    def get_list(self):
        """ Get list of class-list configurations on the device. """
        return self._get(self._build_url())

    def get_all(self):
        """ Get list of class-list configurations on the device. Alias of `self.get_list` method"""
        return self.get_list()

    def all(self):
        """ Get list of class-list configurations on the device. Alias of `self.get_list` method"""
        return self.get_list()

    def exists(self, class_list_name):
        """
        Check class-list configuration with name `class_list_name` existence on the device.

        :param class_list_name: name of the class-list
        :return: True if `class_list_name` class-list exists on the device.
        """
        try:
            self.get(class_list_name)
            return True
        except acos_errors.NotFound:
            return False

    def _build_payload(self, name, file=False, ipv4addr=None, lsn_lid=None, ipv6_addr=None, v6_lsn_lid=None):
        """
        Build and return the payload dictionary to be used to update or create the class-list on the device.

        :param name: name of the class-list going to be created
        :param file: Create/Edit a class-list stored as a file. default 0 and if True 1 else 0
        :param ipv4addr: ipv4 address for ipv4-list
        :param lsn_lid: LSN limit ID for ipv4-list
        :param ipv6_addr: ipv6 address for ipv6-list
        :param v6_lsn_lid: LSN limit ID for ipv6-list
        :return: payload dictionary to be used to update or create the class-list on the device.
        """
        payload = {
            "class-list" : {
                "name": name,
                "file": self.convert_to_int(file),
            }
        }
        if ipv4addr:
            ipv4_elem = {"ipv4addr": ipv4addr}
            if lsn_lid:
                ipv4_elem["lsn-lid"] = lsn_lid

            payload["class-list"]["ipv4-list"] = [ipv4_elem]
        elif ipv6_addr:
            ipv6_elem = {"ipv6-addr": ipv6_addr}
            if v6_lsn_lid:
                ipv6_elem["v6-lsn-lid"] = v6_lsn_lid
            payload["class-list"]["ipv6-list"] = [ipv6_elem]

        return payload
