# Copyright 2014,  Jeff Buttars,  A10 Networks.
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

from acos_client.v30 import base


class OverlayOptions(base.BaseV30):
    url_prefix = "/overlay-tunnel/options"

    def get(self, *args, **kwargs):
        return self._get(self.url_prefix, **kwargs)

    def update(self, gateway_mac, ip_dscp_preserve,
               nvgre_disable_flow_id,
               nvgre_key_mode_lower24,
               tcp_mss_adjust_disable,
               uuid,
               vxlan_dest_port,
               **kwargs):

        options = {}

        if gateway_mac:
            options["gateway-mac"] = gateway_mac

        if ip_dscp_preserve:
            options["ip-dscp-preserve"] = ip_dscp_preserve

        if nvgre_disable_flow_id:
            options["nvgre-disable-flow-id"] = nvgre_disable_flow_id

        if nvgre_key_mode_lower24:
            options["nvgre-key-mode-lower24"] = nvgre_key_mode_lower24

        if tcp_mss_adjust_disable:
            options["tcp-mss-adjust-disable"] = tcp_mss_adjust_disable

        if uuid:
            options["uuid"] = uuid

        if vxlan_dest_port:
            options["vxlan-dest-port"] = vxlan_dest_port

        payload = {
            "options": options
        }

        return self._post(self.url_prefix + "/options", payload, **kwargs)
