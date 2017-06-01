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

import acos_client.errors as acos_errors
import acos_client.v30.base as base


class AFlex(base.BaseV30):
    url_prefix = "/file/aflex"
    elem_name = "aflex"

    def _set(self, file="", content="", size="", action="", **kwargs):

        obj_params = {
            "file": file,
            "size": size,
            "action": action,
        }

        if action in ["create"]:
            obj_params["file-handle"] = file
            obj_params["size"]

        kwargs['params'] = {'aflex': {}}

        for key, val in obj_params.iteritems():
            # Filter out invalid, or unset keys
            if val != "":
                kwargs['params']['aflex'][key] = val

        return self._post(self.url_prefix, file_name=obj_params["file"],
                          file_content=content, **kwargs)


    def get(self, file):
        return self._set(file=file, action="check")

    def exists(self, file):
        try:
            self.get(file)
            return True
        except acos_errors.NotFound:
            return False

    def create(self, file="", content="", size="", action="", **kwargs):
        if self.exists(file):
            raise acos_errors.Exists

        self._set(file, content, size, action="create", **kwargs)

    def delete(self, file):
        self._set(file=file, action="delete")
