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

from acos_client import multipart
import acos_client.v21.base as base


class SSLFile(base.BaseV21):

    def _set(self, action, name, content, filetype, **kwargs):
        m = multipart.Multipart()
        m.file(name="upload_cert", filename=name, value=content)
        ct, payload = m.get()
        kwargs.update(payload=payload, headers={'Content-type': ct})
        return self._post(action, **kwargs)

    def upload(self, name, content, filetype, **kwargs):
        return self._set('slb.ssl.upload', name, content, filetype=filetype,
                         **kwargs)

    def all(self, **kwargs):
        return self._get('slb.ssl.getAll')

