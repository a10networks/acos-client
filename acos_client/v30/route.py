# Copyright 2015, A10 Networks
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


class RIB(base.BaseV30):
    """Manipulation of Routing Information Base"""
    url_prefix = "/ip/route/rib"

    def create(self, destination, mask, next_hops=[]):
        """Create route to {destination} {mask} using {next_hops} expressed as (gateway, distance)"""
        payload = {
            "rib": self._build_payload(destination, mask, next_hops)
        }

        return self._post(self.url_prefix, payload)

    def get(self, destination, mask):
        return self._get(self._build_url(destination, mask))

    def exists(self, destination, mask):
        try:
            self.get(destination, mask)
            return True
        except acos_errors.NotFound:
            return False

    def delete(self, destination, mask):
        return self._delete(self._build_url(destination, mask))

    def update(self, destination, mask, next_hops=[]):
        payload = {
            "rib": self._build_payload(destination, mask, next_hops)
        }
        return self._put(self._build_url(destination, mask), payload)

    def get_all(self):
        return self._get(self.url_prefix)

    def _build_nexthops(self, nexthops):
        hops = []
        for ip, dist in nexthops:
            hops.append({"ip-next-hop": ip, "distance-nexthop-ip": dist})
        return hops

    def _build_payload(self, destination, mask, next_hops):
        hop_array = self._build_nexthops(next_hops)

        payload = {
            "ip-dest-addr": destination,
            "ip-mask": mask
        }

        if len(hop_array) > 0:
            payload["ip-nexthop-ipv4"] = hop_array

        return payload

    def _build_url(self, destination, mask):
        # Self explanatory except the mask. We're trimming the leading / for CIDRs expressed in bits
        # We'd use a URL encoder but it's an edge case.
        return "{urlbase}/{destination}+{mask}".format(
            urlbase=self.url_prefix, destination=destination, mask=mask.replace("/", "%2f"))
