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
from acos_client import errors as acos_errors

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


class MultiLicenseException(Exception):

    def __init__(self):
        self.message = ("Only one of the following attributes can be "
                       "used to define a new license: existing_org, "
                       "existing_user, new_user, or name. These cannot "
                       "be used in conjuction.")
        super(MultiLicenseException, self).__init__()


class NewLicense(base.BaseV30):
    url_prefix = '/glm/new-license'

    def create(self, account_name=None, country=None, existing_org=None,
               glm_password=None, last_name=None, name=None, new_email=None,
               new_password=None, new_user=None, org_id=None, phone=None,
               license_type=None, existing_user=None, first_name=None,
               glm_email=None):
        params = {
            "new-license": {}
        }

        xor = bool(existing_org) + bool(existing_user) + bool(new_user) + bool(name)

        if xor > 1:
            raise MultiLicenseException()

        if existing_org:
            params['new-license'] = self.minimal_dict({
                'existing-org': existing_org,
                'org-id': org_id
            })
        elif existing_user:
            if not glm_email:
                raise acos_errors.RequiredAttributeNotSpecified(
                    self.url_prefix, "existing_user", ["glm_email"])

            params['new-license'] = self.minimal_dict({
                'existing-user': existing_user,
                'glm-email': glm_email,
                'glm-password': glm_password
            })
        elif new_user:
            if not new_email:
                raise acos_errors.RequiredAttributeNotSpecified(
                    self.url_prefix, "new_user", ["new_email"])
            
            params['new-license'] = self.minimal_dict({
                'new-user': new_user,
                'new-email': new_email,
                'new-password': new_password,
                'account-name': account_name,
                'first-name': first_name,
                'last-name': last_name,
                'country': country,
                'phone': phone
            })
        elif name:
            if not license_type:
                raise acos_errors.RequiredAttributeNotSpecified(
                    self.url_prefix, "name", ["license_type"])
            
            params['new-license'] = self.minimal_dict({
                'name': name,
                'type': license_type
            })

        self._post(self.url_prefix, params)