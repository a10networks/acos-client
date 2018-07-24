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


class OverlayVtep(base.BaseV30):
    url_prefix = "/overlay-tunnel/vtep"
    ip_url_format = "{baseurl}/{vtep}/{addrtype}"

    def get(self, vtep_id, *args, **kwargs):
        url = "{0}/{1}".format(self.url_prefix, vtep_id)
        return self._get(url, **kwargs)

    def get_list(self, *args, **kwargs):
        return self._get(self.url_prefix)

    def create(self, vtep_id, source_ip=None, source_vnis=[],
               dest_ips=[], lif_id=None, encap_type="vxlan", **kwargs):
        # vtep_id = ID
        # source_ip = source-ip-address
        # source_vnis = vni-list for source-ip-address
        # dest_ips = list of (ip, [vni_info]) tuples
        # vtep creation can be as simple or complicated as we like
        # we can create a vtep with a minimum of an ID
        # or we can create it with fully populated src/dst info

        is_found = False

        try:
            existing = self.get(vtep_id)
            is_found = existing is not None
        except Exception:
            pass

        if not is_found:
            # Create it.
            payload = {
                "vtep": {
                    "id": vtep_id,
                }
            }
            existing = self._post(self.url_prefix, payload, **kwargs)
        # iterate later.
        dest_ip = dest_ips[0]
        vni = source_vnis[0]
        if source_ip:
            payload, url = self._build_ip_payload_and_url(vtep_id, "source", source_ip, encap_type, vni)
            self._post(url, payload)

        if dest_ip:
            payload, url = self._build_ip_payload_and_url(vtep_id, "destination", dest_ip, encap_type, vni)
            self._post(url, payload)

        return self.get(vtep_id)

    def update(self, vtep_id, ip_address, encap_type="vxlan", **kwargs):
        post_url = "{0}/{vtepid}/destination-ip-address/".format(self.url_prefix, vtepid=vtep_id)
        payload = {
            "destination-ip-address": {
                "ip-address": ip_address,
            }
        }
        return self._post(post_url, payload, **kwargs)

    def delete(self, vtep_id, **kwargs):
        post_url = "{0}/{vtepid}".format(self.url_prefix, vtepid=vtep_id)

        return self._delete(post_url)

    def _add_source_address(self, vtep_id, ip_address, vnis=[]):
        pass

    def _add_destination_address(self, vtep_id, ip_address, vnis=[]):
        pass

    def _add_source_vni(self, vtep_id, ip_address, segment, partition=None, gateway=None, lif=None):
        pass

    def _add_destination_vni(self, vtep_id, ip_address, segment):
        pass

    def _build_ip_payload_and_url(self, vtep_id, target, ip_address, encap_type, vni, lif_id=None):
        addr_type = "{0}-ip-address".format(target)

        payload = {
            addr_type: {
                "ip-address": ip_address,
            }
        }
        if lif_id and target == "source":
            payload[addr_type]["vni-list"] = [{"segment": vni, "partition": "shared", "lif": lif_id}]

        if target == "destination":
            payload[addr_type]["encap"] = encap_type

        url = self.ip_url_format.format(baseurl=self.url_prefix, vtep=vtep_id, addrtype=addr_type)

        return payload, url
