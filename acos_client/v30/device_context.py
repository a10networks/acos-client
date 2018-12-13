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

from acos_client.v30 import base


class DeviceContext(base.BaseV30):
    """Switching of device-contexts"""
    url_prefix = "/device-context"

    def switch(self, device_id, obj_slot_id):
        """Switching of device-context"""
        payload = {
            "device-context": self._build_payload(device_id, obj_slot_id)
        }

        return self._post(self.url_prefix, payload)

    def _build_payload(self, device_id, obj_slot_id):

        payload = {
            "device-id": device_id
        }

        return payload
