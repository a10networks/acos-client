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

    def cli_deploy(self, commandlist, **kwargs):
        payload = {
            "commandlist": commandlist
        }
        return self._post("/clideploy/", payload, **kwargs)