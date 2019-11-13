# Copyright 2019,  Omkar Telee,  A10 Networks.
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

import six

from acos_client import errors as acos_errors
from acos_client.v30 import base


class AFlexPolicy(base.BaseV30):

    url_prefix = '/file/aflex/'

    def get(self, file, **kwargs):
        return self._get(self.url_prefix + file, **kwargs)

    def exists(self, file):
        try:
            self.get(file)
            return True
        except acos_errors.NotFound:
            return False

    def _set(self, file="", script="", size="", action="", **kwargs):

        obj_params = {
            "file": file,
            "size": size,
            "file-handle": file,
            "action": action,
        }
        kwargs['params'] = {'aflex': {}}

        for key, val in six.iteritems(obj_params):
            # Filter out invalid, or unset keys
            if val != "":
                kwargs['params']['aflex'][key] = val
        print(script)
        response = self._post(self.url_prefix, file_name=file,
                              file_content=script, **kwargs)
        return response

    def create(self, file="", script="", size="", action="", **kwargs):
        return self._set(file, script, size, action, **kwargs)

    def update(self, file="", script="", size="", action="", **kwargs):
        return self._set(file, script, size, action, **kwargs)

    def delete(self, l7policyid, **kwargs):
        file = l7policyid
        obj_params = {
            "file": file,
            "action": "delete",
        }
        kwargs['params'] = {'aflex': {}}

        for key, val in six.iteritems(obj_params):
            # Filter out invalid, or unset keys
            if val != "":
                kwargs['params']['aflex'][key] = val

        return self._post(self.url_prefix, file_name=file,
                          file_content="", **kwargs)
