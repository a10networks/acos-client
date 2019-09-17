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

from acos_client import errors as ae
from acos_client.v30 import base


class Action(base.BaseV30):

    def write_memory(self, **kwargs):
        payload = {
            "memory": {
                "destination": "primary",
                "partition": "all"
            }
        }
        try:
            try:
                self._post("/write/memory/", payload, **kwargs)
            except ae.AxapiJsonFormatError:
                # Workaround regression in 4.1.0 backwards compat
                self._post("/write/memory/", "", **kwargs)
        except ae.ConfigManagerNotReady:
            # If the retry loop missed this, catch it next time.
            pass

    def activate_and_write(self, partition, **kwargs):
        self.write_memory()

    def clideploy(self, commandlist, **kwargs):
        payload = {
            "commandlist": commandlist
        }
        return self._post("/clideploy/", payload, **kwargs)

    def reload(self):
        self._post("/reload", "")

    def reboot(self):
        self._post("/reboot", "")

    def setInterface(self, interface):
        data = {"ethernet":{"ifnum": str(interface), "name": "DataPort", "action":"enable", "ip": {"dhcp":1}}}
        url = "/interface/ethernet/" + str(interface)
        self._post(url, data)

    def configureVRRP(self, device_id, set_id):
        data = {"common": { "device-id": device_id, "set-id": set_id, "action":"enable"}}
        url = "/vrrp-a/common"
        self._post(url, data)

    def configureVRID(self, vrid):
        data = { "vrid": { "vrid-val": vrid, "blade-parameters": { "priority":150} } }
        url = "/vrrp-a/vrid"
        self._post(url, data)

    def configSynch(self, ip_address, username, password):
        data = {"sync" : { "address" : ip_address, "auto-authentication" : 1,
                "type" : "all", "usr" : username, "pwd" : password}}
        url = "/configure/sync"
        self._post(url, data)
