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


class Admin(base.BaseV21):

    @property
    def administrator(self):
        return self.Administrator(self.client)

    class Administrator(base.BaseV21):

        def all(self, **kwargs):
            return self._get('system.admin.administrator.getAll', **kwargs)

        def get(self, name, **kwargs):
            params = {"admin_name": name}
            return self._post('system.admin.administrator.search', params, **kwargs)

        def create(self, name, **kwargs):
            params = {
                "administrator": {
                    "admin_name": name
                }
            }

            return self._post('system.admin.administrator.create', params, **kwargs)

        def update(self, name, **kwargs):
            params = {
                "administrator": {
                    "admin_name": name
                }
            }

            return self._post('system.admin.administrator.update', params, **kwargs)

        def delete(self, name, **kwargs):
            params = {"admin_name": name}
            return self._post('system.admin.administrator.delete', params, **kwargs)

        def all_delete(self, **kwargs):
            return self._post('system.admin.administrator.deleteAll', **kwargs)
