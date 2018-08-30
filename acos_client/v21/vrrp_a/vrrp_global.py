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


class VRRPAGlobal(base.BaseV21):
    def get(self, **kwargs):
        return self._get("vrrp_a.get", **kwargs)

    def set(self, status, device_id, set_id, default_vrid, hello_interval, dead_timer,
            track_event_delay, preemption_delay, arp_retry,
            vrid_list={},
            preferred_session_sync_port_list={}):
        params = {
            "vrrp_a": {
                "status": status,
                "device_id": device_id,
                "set_id": set_id,
                "default_vrid": default_vrid,
                "hello_interval": hello_interval,
                "dead_timer": dead_timer,
                "track_event_delay": track_event_delay,
                "preemption_delay": preemption_delay,
                "arp_retry": arp_retry,
            }
        }
        vrids = self._convert_vrid_list(vrid_list)
        sync_ports = self._convert_sync_port_list(preferred_session_sync_port_list)

        if vrids:
            params["vrrp_a"]["vrid_list"] = vrids

        if sync_ports:
            params["vrrp_a"]["preferred_session_sync_port_list"] = sync_ports

        return self._post("vrrp_a.set", params)

    def _convert_vrid_list(self, vrids):
        return vrids

    def _convert_sync_port_list(self, sync_ports):
        return sync_ports
