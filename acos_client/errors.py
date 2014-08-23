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

import acos_client

import v21.responses
import v30.responses


class ACOSException(Exception):
    def __init__(self, code=1, msg=''):
        self.code = code
        self.msg = msg
        super(ACOSException, self).__init__(msg)


class ACOSUnsupportedVersion(ACOSException):
    pass


class ACOSUnknownError(ACOSException):
    pass


class AddressSpecifiedIsInUse(ACOSException):
    pass


class AuthenticationFailure(ACOSException):
    pass


class InvalidSessionID(ACOSException):
    pass


class Exists(ACOSException):
    pass


class NotFound(ACOSException):
    pass


class NoSuchServiceGroup(ACOSException):
    pass


class InUse(ACOSException):
    pass


class InvalidPartitionParameter(ACOSException):
    pass


class MemoryFault(ACOSException):
    pass


class InvalidParameter(ACOSException):
    pass


RESPONSE_CODE_MAP = {
    acos_client.AXAPI_21: v21.responses.RESPONSE_CODES,
    acos_client.AXAPI_30: v30.responses.RESPONSE_CODES,
}


def raise_axapi_ex(version, response, action=None):
    response_codes = RESPONSE_CODE_MAP[version]

    if 'response' in response and 'err' in response['response']:
        code = response['response']['err']['code']

        if code in response_codes:
            ex_dict = response_codes[code]
            ex = None

            if action is not None and action in ex_dict:
                ex = ex_dict[action]
            else:
                for k in ex_dict.keys():
                    if action.startswith(k):
                        ex = ex_dict[k]

                if not ex and '*' in ex_dict:
                    ex = ex_dict['*']

            if ex is not None:
                raise ex(code, response['response']['err']['msg'])
            else:
                return

        raise ACOSException(code, response['response']['err']['msg'])

    raise ACOSException()
