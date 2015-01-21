# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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


from action import Action
import base
from config_file import ConfigFile
from device_info import DeviceInfo
from log import Log
from partition import Partition

import acos_client.multipart as multipart


class System(base.BaseV21):
    def backup(self, **kwargs):
        return self._get("system.backup", **kwargs)

    def restore(self, name, data, **kwargs):
        m = multipart.Multipart()
        m.file(name="restore", filename=name, value=data)
        ct, payload = m.get()
        kwargs.update(payload=buffer(payload), headers={'Content-Type': ct})
        return self._post("system.restore", **kwargs)

    def tech_download(self, **kwargs):
        return self._get("system.show_tech.download", **kwargs)

    def information(self):
        return self._get("system.information.get")

    @property
    def device_info(self):
        return DeviceInfo(self.client)

    @property
    def action(self):
        return Action(self.client)

    @property
    def partition(self):
        return Partition(self.client)

    @property
    def config_file(self):
        return ConfigFile(self.client)

    @property
    def log(self):
        return Log(self.client)

    @property
    def banner(self):
        return self.Banner(self.client)

    class Banner(base.BaseV21):
        def get(self, **kwargs):
            return self._get('system.banner.get', **kwargs)

        def set(self, banner, **kwargs):
            params = {"banner": banner}
            return self._post('system.log.banner.set', params, **kwargs)

    @property
    def hostname(self):
        return self.Hostname(self.client)

    class Hostname(base.BaseV21):
        def get(self, **kwargs):
            return self._get('system.hostname.get', **kwargs)

        def set(self, hostname, **kwargs):
            params = {"hostname": hostname}
            return self._post('system.hostname.set', params, **kwargs)
