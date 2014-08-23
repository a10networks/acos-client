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

import acos_client.errors as ae


RESPONSE_CODES = {
    1023410176: {
        '/axapi/v3/slb/service-group/': ae.NoSuchServiceGroup,
        '*': ae.NotFound
    },
    1023475722: {
        '*': ae.NotFound
    },
    1207959957: {
        '*': ae.NotFound
    },
}


def raise_axapi_auth_error(response, action=None, headers={}):
    if 'authorizationschema' in response:
        if response['authorizationschema']['code'] == 401:
            if 'Authorization' in headers:
                raise ae.InvalidSessionID()
            else:
                raise ae.AuthenticationFailure()
        elif response['authorizationschema']['code'] == 403:
            raise ae.AuthenticationFailure()
