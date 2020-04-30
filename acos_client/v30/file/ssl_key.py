# Copyright 2015,  Tobit Raff,  A10 Networks.
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


class SSLKey(base.BaseV30):

    url_prefix = '/file/ssl-key/'

    def get(self, file):
        return self._get(self.url_prefix + file)

    def exists(self, file):
        try:
            self.get(file)
            return True
        except acos_errors.NotFound:
            return False

    def _set(self, file="", cert="", size="", action="", **kwargs):

        obj_params = {
            "file": file,
            "size": size,
            "file-handle": file,
            "action": action,
        }

        kwargs['params'] = {'ssl-key': {}}

        for key, val in six.iteritems(obj_params):
            # Filter out invalid, or unset keys
            if val != "":
                kwargs['params']['ssl-key'][key] = val

        return self._post(self.url_prefix, file_name=obj_params["file"],
                          file_content=cert, **kwargs)

    def create(self, file="", cert="", size="", action=""):
        if self.exists(file):
            raise acos_errors.Exists

        self._set(file, cert, size, action)

    def update(self, file="", cert="", size="", action=""):
        self._set(file, cert, size, action)

    def delete(self, private_key=""):
        payload = {"delete": {"private-key": private_key}}
        self._request("POST", "/pki/delete", payload)
