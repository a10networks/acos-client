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


class ConfigFile(base.BaseV21):

    def upload(self, cfg_backup, **kwargs):
        return self._post("system.config_file.upload", cfg_backup, **kwargs)

    def restore(self, **kwargs):
        return self._post("system.config_file.restore", **kwargs)

    def write(self, from_file, to_file, **kwargs):
        return self._post("system.config_file.write",
                          {"from": from_file, "to": to_file}, **kwargs)
