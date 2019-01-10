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


class Vlan(base.BaseV30):
    def __init__(self, client):
        super(Vlan, self).__init__(client)
        self.url_prefix = "/network/vlan"

    def _build_id_url(self, vlan_id):
        return "{0}/{1}".format(self.url_prefix, vlan_id)

    def get_list(self):
        return self._get(self.url_prefix)

    def create(self, vlan_id, name=None, shared_vlan=False,
               untagged_eths=[], untagged_trunks=[],
               tagged_eths=[], tagged_trunks=[], veth=False,
               lif=None):

        payload = {
            "vlan": self._build_payload(
                name, vlan_id, shared_vlan, untagged_eths,
                untagged_trunks,
                tagged_eths, tagged_trunks,
                veth, lif)
        }
        return self._post(self.url_prefix, payload)

    def get(self, vlan_id):
        return self._get(self._build_id_url(vlan_id))

    def exists(self, vlan_id):
        try:
            self.get(vlan_id)
            return True
        except acos_errors.NotFound:
            return False

    def delete(self, vlan_id):
        return self._delete(self._build_id_url(vlan_id))

    def _build_payload(self, name, vlan_id, shared_vlan,
                       untagged_eths, untagged_trunks,
                       tagged_eths, tagged_trunks,
                       veth, lif):
        rv = {
            "vlan-num": vlan_id,
        }

        if name:
            rv["name"] = name

        if shared_vlan is True:
            rv["shared-vlan"] = shared_vlan

        if untagged_eths:
            rv.update(self._build_range_list("untagged-eth", untagged_eths, "untagged-ethernet"))

        if tagged_eths:
            rv.update(self._build_range_list("tagged-eth", tagged_eths, "tagged-ethernet"))

        if untagged_trunks:
            rv.update(self._build_range_list("untagged-trunk", untagged_trunks))

        if tagged_trunks:
            rv.update(self._build_range_list("tagged-trunk", tagged_trunks))

        if veth:
            rv["ve"] = vlan_id

        if lif:
            rv["untagged-lif"] = lif

        return rv

    def _build_range_list(self, prefix="", xlist=[], inconsistent_prefix=""):
        # Naive way of building this poorly-conceived API call
        rv = []
        ekey_f = "{0}-list"
        rkey_f = "{0}-{1}"

        # Justification for snarky prefix
        fix_prefix = lambda: inconsistent_prefix if inconsistent_prefix else prefix

        for x in xlist:
            lm = {}
            lm[rkey_f.format(fix_prefix(), "start")] = x
            lm[rkey_f.format(fix_prefix(), "end")] = x
            rv.append(lm)

        return {ekey_f.format(prefix): rv}
