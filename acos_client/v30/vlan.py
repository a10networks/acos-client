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

from acos_client.v30 import base


class Vlan(base.BaseV30):
    def __init__(self):
        self.url_prefix = "/network/vlan"

    def _build_id_url(self, vlan_id):
        return "{0}/{1}".format(self.url_prefix, vlan_id)

    def get_list(self):
        return self._get(self.url_prefix)

    def create(self, vlan_id, shared_vlan=False, 
               untagged_eths=[], untagged_trunks=[], 
               tagged_eths=[], tagged_trunks=[], veth_interface=None,
               logical_interface=None):
        payload = self._build_payload(vlan_id, shared_vlan, untagged_eths, 
                                      untagged_trunks,
                                      tagged_eths, tagged_trunks, 
                                      veth_interface, logical_interface)

    def get(self, vlan_id):
        return self._get(self._build_id_url(vlan_id))

    def delete(self, vlan_id):
        return self._delete(self._build_id_url(vlan_id))

    def _build_payload(self, vlan_id, shared_vlan, 
                       untagged_eths, untagged_trunks,
                       tagged_eths, tagged_trunks,
                       veth_interface, logical_interface):
        rv = {
                "vlan_num": vlan_id,
        }
       
        if shared_vlan:
            rv["shared-vlan"] = shared_vlan 

        if untagged_eths:
            rv.update(self._build_range_list("untagged-ethernet", untagged_eths))

        if tagged_eths:
            rv.update(self._build_range_list("tagged-ethernet", tagged_eths))

        if untagged_trunks:
            rv.update(self._build_range_list("untagged-trunk", untagged_trunks))

        if tagged_trunks:
            rv.update(self._build_range_list("tagged-trunk", untagged_trunks))

        if veth_interface:
            rv["ve"] = veth_interface

        if logical_interface:
            rv["untagged-lif"] = logical_interface

        return rv

    def _build_range_list_dict(self, prefix="", xlist=[]):
        # Naive way of building this poorly-conceived API call
        rv = []
        rkey_f = "{0}-{1}"
        for x in xlist:
            lm = {}
            lm[rvkey_f.format(prefix, "start")] = x
            lm[rvkey_f.format(prefix, "end")] = x
            rv.append(lm)
        return {prefix: rv}
