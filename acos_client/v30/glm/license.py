# Copyright (C) 2021, A10 Networks Inc. All rights reserved.

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

from acos_client.v30 import base


class LicenseRequest(base.BaseV30):
    url_prefix = '/glm/create-license-request'

    def _set(self, create_license_request):
        params = {
            'create-license-request': create_license_request
        }

        return params

    def create(self, create_license_request=None,  **kwargs):
        params = self._set(create_license_request=None)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def update(self, create_license_request=None, **kwargs):
        params = self._set(create_license_request=None)
        return self._post(self.url_prefix, params, axapi_args=kwargs)

    def put(self, create_license_request=None, **kwargs):
        params = self._set(create_license_request=None)
        return self._put(self.url_prefix, params, axapi_args=kwargs)

    def delete(self):
        return self._delete(self.url_prefix)


class NewLicense(base.BaseV30):
    url_prefix = '/glm/send'

    def create(self, license_request=None):
        params = {
            "send": self.minimal_dict({
                "license-request": license_request
            })
        }

        self._post(self.url_prefix, params)