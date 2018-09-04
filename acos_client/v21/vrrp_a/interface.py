# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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


class VRRPAInterface(base.BaseV21):
    def get_all(self, **kwargs):
        return self._get("vrrp_a.interface.getAll", **kwargs)

    def search(self, interface_num):
        params = {"interface_number": interface_num}

        return self._post("vrrp_a.interface.search", params)

    def update(self, interface_number, interface_type, status, vrrp_a_status, link_type, heartbeat, vlan=None):
        env_val = "vrrp_a_interface"
        params = {
            env_val: {
                "interface_number": interface_number,
                "interface_type": interface_type,
                "status": status,
                "vrrp_a_status": vrrp_a_status,
                "link_type": link_type,
                "heartbeat": heartbeat
            }
        }

        if vlan:
            params[env_val]["vlan"] = vlan

        return self._post("vrrp_a.interface.update", params)
