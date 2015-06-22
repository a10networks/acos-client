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

import json
import re

from acos_client import multipart
import acos_client.v21.base as base


class ClassList(base.BaseV21):

    @staticmethod
    def _fix_json(data):
        p = re.compile(r'(?<=[^:{\[,])"(?![:,}\]])')
        return json.loads(re.sub(p, '\\"', data))

    def all(self, **kwargs):
        return self._fix_json(self._get("slb.class_list.getAll", **kwargs))

    def get(self, name, **kwargs):
        return ClassList._fix_json(self._post("slb.class_list.search",
                                              {'name': name}, **kwargs))

    def download(self, name, **kwargs):
        return self._post('slb.class_list.download',
                          params={'file_name': name}, **kwargs)

    def upload(self, name, class_list, **kwargs):
        m = multipart.Multipart()
        m.file(name=name, filename=name, value=class_list)
        ct, payload = m.get()
        kwargs.update(payload=payload, headers={'Content-type': ct})
        return self._post('slb.class_list.upload', **kwargs)

    def _set(self, action, class_list, **kwargs):
        return self._post(action, class_list, **kwargs)

    def create(self, class_list, **kwargs):
        return self._set("slb.class_list.create", class_list, **kwargs)

    def update(self, class_list, **kwargs):
        return self._set("slb.class_list.update", class_list, **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.class_list.delete", {"name": name}, **kwargs)
