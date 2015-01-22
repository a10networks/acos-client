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


class DeviceInfo(base.BaseV21):

        def get(self, **kwargs):
            return self._get('system.device_info.get', **kwargs)

        def cpu_current_usage(self, **kwargs):
            return self._get('system.device_info.cpu.current_usage.get',
                             **kwargs)

        def cpu_historical_usage(self, **kwargs):
            return self._get('system.device_info.cpu.historical_usage.get',
                             **kwargs)
