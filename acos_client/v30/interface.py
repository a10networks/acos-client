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

from ipaddress import IPv4Interface


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

    def create(
        self,
        ifnum, name=None,
        enable=None,
        ipv4_address=None,
        dhcp=None,
        ipv4_nat_inside=None,
        ipv6_address=None,
        ipv6_nat_inside=None,
    ):
        """
        CREATE a VE interface with the provided values.
        Don't forget to create that interface form VLAN config, otherwise
        will fail to create
        :param ifnum: Interface number, according with VLAN ID [2-4094]
        :param name: (Optional) Set the name of the interface
        :param enable: (Optional) Enable interface
        :param ipv4_address: (Optional) List of Tuples that stores IPv4 Address and IPv4 Netmask
            of that interface. E.g ('192.168.255.1', '255.255.255.252')
            OR List os IPs provided in the <host_ip>/<netmask> format. E.g ["10.1.11.1/24", "12.12.12.12/28"]
        :param dhcp: (Optional) Enable DHCP on the interface
        :param ipv4_nat_inside: (Optional) Enable Inside NAT on IPv4
        :param ipv6_address: (Optional) List of strs that stores IPv6 Addresses info in the
            following format: 'FE81::1/64'
        :param ipv6_nat_inside: (Optional) Enable Inside NAT on IPv6
        """
        payload = self._build_payload(
            ifnum=ifnum, name=name,
            enable=enable,
            ipv4_address=ipv4_address,
            dhcp=dhcp,
            ipv4_nat_inside=ipv4_nat_inside,
            ipv6_address=ipv6_address,
            ipv6_nat_inside=ipv6_nat_inside
        )
        return self._post(self.url_prefix, payload)

    def update(
        self,
        ifnum, name=None,
        enable=None,
        ipv4_address=None,
        dhcp=None,
        ipv4_nat_inside=None,
        ipv6_address=None,
        ipv6_nat_inside=None
    ):
        """
        Update a VE interface with the provided values.
        Don't forget to create that interface form VLAN config, otherwise
        will fail to create
        :param ifnum: Interface number, according with VLAN ID [2-4094]
        :param name: (Optional) Set the name of the interface
        :param enable: (Optional) Enable interface
        :param ipv4_address: (Optional) List of Tuples that stores IPv4 Address and IPv4 Netmask
            of that interface. E.g ('192.168.255.1', '255.255.255.252')
            OR List os IPs provided in the <host_ip>/<netmask> format. E.g ["10.1.11.1/24", "12.12.12.12/28"]
        :param dhcp: (Optional) Enable DHCP on the interface
        :param ipv4_nat_inside: (Optional) Enable Inside NAT on IPv4
        :param ipv6_address: (Optional) List of strs that stores IPv6 Addresses info in the
            following format: 'FE81::1/64'
        :param ipv6_nat_inside: (Optional) Enable Inside NAT on IPv6
        """
        payload = self._build_payload(
            ifnum=ifnum, name=name,
            enable=enable,
            ipv4_address=ipv4_address,
            dhcp=dhcp,
            ipv4_nat_inside=ipv4_nat_inside,
            ipv6_address=ipv6_address,
            ipv6_nat_inside=ipv6_nat_inside
        )
        return self._post(f"{self.url_prefix}{ifnum}", payload)

    def _build_payload(
        self,
        ifnum,
        name=None,
        enable=None,
        ipv4_address=None,
        dhcp=None,
        ipv4_nat_inside=None,
        ipv6_address=None,
        ipv6_nat_inside=None
    ):
        rv = {
            self.iftype: {
                "ifnum": ifnum
            }
        }
        if enable is not None:
            rv[self.iftype].update(
                {
                    "action": "enable" if enable is True else "disable"
                }
            )
        if name is not None:
            rv[self.iftype].update(
                {
                    "name": name
                }
            )
        if ipv4_address is not None and dhcp is None:
            if isinstance(ipv4_address, tuple):
                rv[self.iftype].update(
                    {
                        "ip": {
                            "address-list": [
                                {
                                    "ipv4-address": ip,
                                    "ipv4-netmask": netmask
                                }
                                for ip, netmask in ipv4_address
                            ]
                        }
                    }
                )
            else:
                rv[self.iftype].update(
                    {
                        "ip": {
                            "address-list": [
                                {
                                    "ipv4-address": str(ip.ip),
                                    "ipv4-netmask": str(ip.netmask)
                                }
                                for ip in map(lambda x: IPv4Interface(x), ipv4_address)
                            ]
                        }
                    }
                )
            if ipv4_nat_inside is not None:
                rv[self.iftype]['ip'].update(
                    {
                        "inside": 1 if ipv4_nat_inside is True else 0
                    }
                )
        elif ipv4_address is None and dhcp is not None:
            rv[self.iftype].update(
                {
                    "ip": {
                        "dhcp": 1 if dhcp is True else 0
                    }
                }
            )
        if ipv6_address is not None:
            rv[self.iftype].update(
                {
                    "ipv6": {
                        "address-list": [
                            {
                                "ipv6-addr": ipv6,
                            }
                            for ipv6 in ipv6_address
                        ],
                    }
                }
            )
            if ipv6_nat_inside is not None:
                rv[self.iftype]['ipv6'].update(
                    {
                        "inside": 1 if ipv4_nat_inside is True else 0
                    }
                )
        return rv
