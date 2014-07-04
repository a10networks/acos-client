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

import logging
LOG = logging.getLogger(__name__)

import sys
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setLevel(logging.DEBUG)
LOG.addHandler(out_hdlr)

LOG.setLevel(logging.DEBUG)


class ACOSException(Exception):
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
    1009: {
        'session.close': None,
        '*': InvalidSessionID
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
        '*': NotFound
    },
    67305473: {
        'slb.service_group.delete': None,
        'slb.service_group.member.create': NoSuchServiceGroup,  ## ?? 2.7.1
        'slb.service_group.member.delete': None,
        '*': NotFound
    },
    402653200: {
        '*': Exists
    },
    402653201: {
        '*': Exists
    },
    402653206: {
        '*': Exists
    },
    520486915: {
        '*': AuthenticationFailure  # /authenticate, 2.7.1
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

            LOG.debug("raise_axapi_ex method=%skipping", action)

            if action is not None and action in ex_dict:
                ex = ex_dict[action]
            elif '*' in ex_dict:
                ex = ex_dict['*']

            if ex is not None:
                raise ex
            else:
                LOG.debug("raise_axapi_ex skipping error: %s, %s", action, response)
                return

    raise ACOSException()
