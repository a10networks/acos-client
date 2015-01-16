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

import acos_client.errors as acos_errors

import base


class Action(base.BaseV21):

    def write_memory(self):
        try:
            self._get("system.action.write_memory")
        except acos_errors.InvalidPartitionParameter:
            pass

    def reboot(self, **kwargs):
        raise NotImplementedError
        # return self._post("system.action.reboot", **kwargs)

    def reload(self, write_memory=False, **kwargs):
        # write_memory param is required but no matter what value is passed
        # it will ALWAYS save pending changes
        write_memory = 1 if write_memory else 0
        return self._post("system.action.reload",
                          params={"write_memory": write_memory}, **kwargs)
