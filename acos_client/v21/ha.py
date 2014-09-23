# Copyright 2014,  Doug Wiegley,  A10 Networks.
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

import base


class HA(base.BaseV21):

    def sync(self, destination_ip, username, password):
        params = {
            "ha_config_sync": {
                "auto_authentication": 0,
                "user": username,
                "password": password,
                "sync_all_partition": 1,
                "operation": 2,  # running config only
                "peer_operation": 0,  # running config
                "peer_reload": 0,
                "destination_ip": destination_ip
            }
        }

        self._post('ha.sync_config', params)
