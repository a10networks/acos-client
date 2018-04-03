# -*- coding: utf-8 -*-

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

import random
import time
import acos_client.errors as acos_errors
import base


class DeviceContext(base.BaseV30):
    def __init__(self, client):
        super(DeviceContext, self).__init__(client)
        self.url_prefix = "/device-context/"

    def switch_context(self, device_id='1'):
        params = {
            "device-context":
                {
                    "device-id": device_id
                }
        }
        self._post(self.url_prefix, params)