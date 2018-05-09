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

from acos_client.v21 import base


class Interface(base.BaseV21):
    def _build_payload(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
                       speed="auto", **kwargs):
        cli_cmds = []

        if ifnum:
            cli_cmds += ["interface ethernet {port_num}".format(port_num=ifnum)]
        if ip_address and not dhcp:
            cli_cmds += ['ip address {ip} {mask}'.format(ip=ip_address,
                                                         mask=ip_netmask)]
        elif dhcp:
            cli_cmds += ['ip address dhcp']
        cli_cmds += ['write mem']
        return "\n".join(cli_cmds)

    def get_list(self):
        return self._get('network.interface.getAll')

    def get(self, ifnum=None):
        params = {
            "port_num": ifnum
        }
        return self._post('network.interface.get', params=params)

    def delete(self, ifnum):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    def create(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enabled=enable, speed=speed)
        return self._post("cli.deploy", params=None,
                          payload=payload)

    def update(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed)
        return self._request("POST", "cli.deploy", params=None, payload=payload)

    @property
    def ethernet(self):
        return EthernetInterface(self.client)

    @property
    def management(self):
        return ManagementInterface(self.client)


class EthernetInterface(Interface):
    pass


class ManagementInterface(Interface):
    def _build_payload(self, ifnum=None, ip_address=None, ip_netmask=None, ip_gateway=None,
                       dhcp=False, enable=None, speed="auto", apps_use_mgmt_port=True, **kwargs):
        # TODO(mdurrant) - Check ip/netmask for validity.
        rv = {
            "status": 1,
        }

        rv["speed"] = speed
        rv["apps_use_mgmt_port"] = 1 if apps_use_mgmt_port else 0

        if ip_address and not dhcp:
            rv["ipv4_address"] = ip_address
            rv["ipv4_netmask"] = ip_netmask
            rv["ipv4_gateway"] = ip_gateway
        else:
            rv["ipv4_address"] = "dhcp"

        return {"mgmt_interface": rv}

    def get(self):
        return self._get('network.mgmt_interface.get')

    def create(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto", default_gateway=None):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enabled=enable, speed=speed,
                                      default_gateway=default_gateway)
        return self._post("network.mgmt_interface.set",
                          payload)

    def update(self, ifnum=None, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto", default_gateway=None):
        payload = self._build_payload(ifnum=ifnum, ip_address=ip_address, ip_netmask=ip_netmask,
                                      dhcp=dhcp, enable=enable, speed=speed,
                                      default_gateway=default_gateway)
        return self._post("network.mgmt_interface.set",
                          payload)
