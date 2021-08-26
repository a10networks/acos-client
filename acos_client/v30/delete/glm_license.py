# Copyright (C) 2021, A10 Networks Inc. All rights reserved.

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


class DeleteGLMLicense(base.BaseV30):
    url_prefix = '/delete/glm-license/'

    def post(self, a10_ti=None, ipsec_vpn=None, qosmos=None,
             threatstop=None, webroot=None, webroot_ti=None,
             max_retries=None, timeout=None, **kwargs):
        params = {
            "glm-license": self.minimal_dict({
                "a10-ti": a10_ti,
                "ipsec-vpn": ipsec_vpn,
                "qosmos": qosmos,
                "threatstop": threatstop,
                "webroot": webroot,
                "webroot-ti": webroot_ti
            }),
        }

        if not params['glm-license']:
            params = {}

        self._post(self.url_prefix, params, max_retries=max_retries,
                   timeout=timeout, axapi_args=kwargs)
