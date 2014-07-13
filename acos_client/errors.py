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


class ACOSException(Exception):
    def __init__(self, code=1, msg=''):
        self.code = code
        self.msg = msg


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


RESPONSE_CODES = {
    999: {
        '*': NotFound
    },
    1009: {
        'session.close': None,
        '*': InvalidSessionID
    },
    1023: {
        'slb.service_group.member.delete': None,
        '*': NotFound
    },
    1043: {
        'slb.virtual_server.vport.delete': None,
        '*': NotFound
    },
    1405: {
        '*': Exists
    },
    1406: {
        '*': Exists
    },
    1982: {
        '*': Exists
    },
    2941: {
        '*': Exists
    },
    33619968: {
        'slb.hm.delete': None,
        '*': NotFound
        },
    67174402: {
        'slb.server.delete': None,
        '*': NotFound
    },
    67239937: {
        'slb.virtual_server.delete': None,
        'slb.virtual_service.delete': None,
        '*': NotFound
    },
    67239947: {
        '*': Exists
    },
    67305473: {
        'slb.service_group.delete': None,
        'slb.service_group.member.create': NoSuchServiceGroup,
        'slb.service_group.member.update': NoSuchServiceGroup,
        '*': NotFound
    },
    67371009: {
        'slb.template.cookie_persistence.delete': None,
        'slb.template.src_ip_persistence.delete': None,
        '*': NotFound
    },
    402653200: {
        '*': Exists
    },
    402653201: {
        '*': Exists
    },
    402653202: {
        '*': Exists
    },
    402653206: {
        '*': Exists
    },
    402718800: {
        '*': NotFound
    },
    520486915: {
        '*': AuthenticationFailure
    },
    520749062: {
        '*': NotFound
    },
    654311465: {
        '*': AddressSpecifiedIsInUse
    },
    654311496: {
        '*': AddressSpecifiedIsInUse
    },
}


def raise_axapi_ex(response, action=None):
    if 'response' in response and 'err' in response['response']:
        code = response['response']['err']['code']

        if code in RESPONSE_CODES:
            ex_dict = RESPONSE_CODES[code]
            ex = None

            if action is not None and action in ex_dict:
                ex = ex_dict[action]
            elif '*' in ex_dict:
                ex = ex_dict['*']

            if ex is not None:
                raise ex(code, response['response']['err']['msg'])
            else:
                return

        raise ACOSException(code, response['response']['err']['msg'])
    raise ACOSException()
