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
import six


from acos_client import errors as acos_errors
from acos_client.v30 import base


class OverlayVtep(base.BaseV30):
    url_prefix = "/overlay-tunnel/vtep"

    def get(self, vtep_id, *args, **kwargs):
        return self._get(self.url_prefix, **kwargs)

    def get_list(self, *args, **kwargs):
        return self._get(self.url_prefix) 

    def create(self, vtep_id, ip_address, encap_type="vxlan"):
        payload = {
            "destination-ip-address": {
                "ip-address": ip_address,
                "encap": encap_type
            }
        }

        post_url = "{0}/{vtepid}/destination-ip-address".format(self.url_prefix, vtepid=vtep_id)
        
        return self._post(post_url, payload, **kwargs)

    def update(self, vtep_id, ip_address, encap_type="vxlan", **kwargs):
        post_url = "{0}/{vtepid}/destination-ip-address/".format(self.url_prefix, vtepid=vtep_id)
        payload = {
            "destination-ip-address": {
                "ip-address": ip_address,
                "encap": encap_type
            }
        }
        return self._post(post_url, payload, **kwargs)

    def delete(self, vtep_id, ip_address, **kwargs):
        post_url = "{0}/{vtepid}/destination-ip-address/{ip}".format(self.url_prefix, vtepid=vtep_id, ip=ip_address)

        return self._delete(post_url)
