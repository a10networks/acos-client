# Copyright 2016, A10 Networks
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


class Interface(base.BaseV30):
    iftype = "interface"
    url_prefix = "/interface/"

    def __init__(self, client):
        super(Interface, self).__init__(client)

    def _url_from_ifnum(self, ifnum=None):
        return self.url_prefix + self._ifnum_to_str(ifnum)

    def _ifnum_to_str(self, ifnum=None):
        return str(ifnum if ifnum else "")

    def _build_payload(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
                       speed="auto", **kwargs):
        # TODO(mdurrant) - Check ip/netmask for validity.
        rv = {
            "interface": {
                "ip": {
                }
            }
        }

        if ifnum:
            rv["interface"]["ifnum"] = ifnum
        if ip_address and not dhcp:
            rv["interface"]["ip"]["address-list"] = [
                {"ipv4-address": ip_address, "ipv4-netmask": ip_netmask}
            ]
        else:
            rv["interface"]["ip"]["dhcp"] = 1 if dhcp is True else 0

        if enable is not None:
            rv["interface"]["action"] = "enable" if enable else "disable"

        return rv

    def get_list(self):
        return self._get(self.url_prefix)

    def get(self, ifnum=None):
        return self._get(self._url_from_ifnum(ifnum))

    def exists(self, ifnum=None):
        try:
            self.get(ifnum)
            return True
        except acos_errors.NotFound:
            return False

    def delete(self, ifnum):
        url = self.url_prefix + self._ifnum_to_str(ifnum)
        return self._delete(url)

    def create(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):

        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed)
        return self._post(self.url_prefix, payload)

    def update(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed)
        return self._post(self.url_prefix + self._ifnum_to_str(ifnum),
                          payload)

    def get_oper(self, ifnum):
        url = "{0}{1}/oper".format(self.url_prefix, ifnum)
        return self._get(url)

    @property
    def ethernet(self):
        return EthernetInterface(self.client)

    @property
    def management(self):
        return ManagementInterface(self.client)

    @property
    def lif(self):
        return LogicalInterface(self.client)

    @property
    def ve(self):
        return VirtualEthernet(self.client)


class EthernetInterface(Interface):
    def __init__(self, client):
        super(EthernetInterface, self).__init__(client)
        self.iftype = "ethernet"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)

    def _build_payload(self, **kwargs):
        rv = super(EthernetInterface, self)._build_payload(**kwargs)
        # Allows us to use the Interface class for ethernet ifs
        rv[self.iftype] = rv.pop("interface")
        return rv


class ManagementInterface(Interface):
    def __init__(self, client):
        super(ManagementInterface, self).__init__(client)
        self.iftype = "management"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)

    def _build_payload(self, **kwargs):
        rv = super(ManagementInterface, self)._build_payload(**kwargs)
        # Allows us to use the Interface class for management ifs
        rv[self.iftype] = rv.pop("interface")
        default_gateway = kwargs.get("default_gateway")
        if default_gateway:
            rv[self.iftype]["ip"]["default-gateway"] = default_gateway

        return rv

    def create(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto", default_gateway=None):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed,
                                      default_gateway=default_gateway)
        return self._post(self.url_prefix,
                          payload)

    def update(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto", default_gateway=None):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed,
                                      default_gateway=default_gateway)
        return self._post(self.url_prefix + self._ifnum_to_str(ifnum),
                          payload)


class LogicalInterface(Interface):
    def __init__(self, client):
        super(LogicalInterface, self).__init__(client)
        self.iftype = "lif"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)

    def create(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto", default_gateway=None):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed,
                                      default_gateway=default_gateway)
        return self._post(self.url_prefix, payload)

    def _build_payload(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False,
                       enable=None, speed="auto", default_gateway=None):
        # TODO(mdurrant) - Check ip/netmask for validity.
        rv = {
            self.iftype: {
                "ip": {
                }
            }
        }

        if ifnum:
            rv[self.iftype]["ifnum"] = ifnum
        if ip_address and not dhcp:
            rv[self.iftype]["ip"]["address-list"] = [
                {"ipv4-address": ip_address, "ipv4-netmask": ip_netmask}
            ]
        else:
            rv[self.iftype]["ip"]["dhcp"] = 1 if dhcp is True else 0

        if enable is not None:
            rv[self.iftype]["action"] = "enable" if enable else "disable"

        return rv


class VirtualEthernet(Interface):
    def __init__(self, client):
        super(VirtualEthernet, self).__init__(client)
        self.iftype = "ve"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)

    def _build_payload(self, **kwargs):
        # we need to deal with VLAN stuff here
        rv = super(VirtualEthernet, self)._build_payload(**kwargs)
        rv[self.iftype] = rv.pop("interface")

        return rv
