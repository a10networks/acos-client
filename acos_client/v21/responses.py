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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as ae

RESPONSE_CODES = {
    999: {
        '*': ae.NotFound
    },
    1002: {
        '*': ae.MemoryFault
    },
    1009: {
        'session.close': None,
        '*': ae.InvalidSessionID
    },
    1023: {
        'slb.service_group.member.delete': None,
        '*': ae.NotFound
    },
    1043: {
        'slb.virtual_server.vport.delete': None,
        '*': ae.NotFound
    },
    1076: {
        'session.close': None,
        '*': ae.InvalidPartitionParameter
    },
    1162: {
        '*': ae.InvalidInteger
    },
    1163: {
        '*': ae.InvalidParameter
    },
    1165: {
        '*': ae.HMMissingHttpPassive
    },
    1405: {
        '*': ae.Exists
    },
    1406: {
        '*': ae.Exists
    },
    1982: {
        '*': ae.Exists
    },
    2004: {
        '*': ae.InUse
    },
    2035: {
        '*': ae.InUse
    },
    2941: {
        '*': ae.Exists
    },
    3602: {
        'slb.class_list.update': ae.NotFound,
        '*': ae.NotFound
    },
    17039361: {
        'slb.aflex.delete': None,
        '*': ae.NotFound
    },
    17039364: {
        'slb.aflex.upload': ae.InUse,
        'slb.aflex.delete': ae.InUse,
        '*': ae.InUse
    },
    33619968: {
        'slb.hm.delete': None,
        '*': ae.NotFound
    },
    33619969: {
        '*': ae.InUse,
    },
    67174402: {
        'slb.server.delete': None,
        'slb.server.port.delete': None,
        '*': ae.NotFound
    },
    67239937: {
        'slb.virtual_server.delete': None,
        'slb.virtual_service.delete': None,
        'slb.virtual_service.update': ae.NotFound,
        '*': ae.NotFound
    },
    67239947: {
        '*': ae.Exists
    },
    67239962: {
        '*': ae.NotFound
    },
    67239963: {
        '*': ae.CertificateParsingFailed
    },
    67239965: {
        '*': ae.KeyParsingFailed
    },
    67305473: {
        'slb.service_group.delete': None,
        'slb.service_group.member.delete': None,
        'slb.service_group.member.create': ae.NotFound,
        'slb.service_group.member.update': ae.NotFound,
        '*': ae.NotFound
    },
    67371009: {
        'slb.template.cookie_persistence.delete': None,
        'slb.template.src_ip_persistence.delete': None,
        'slb.template.client_ssl.delete': None,
        'slb.template.server_ssl.delete': None,
        '*': ae.NotFound
    },
    67371049: {
        'slb.class_list.delete': None,
        '*': ae.NotFound
    },
    402653200: {
        '*': ae.Exists
    },
    402653201: {
        '*': ae.Exists
    },
    402653202: {
        '*': ae.Exists
    },
    402653206: {
        '*': ae.Exists
    },
    402718800: {
        '*': ae.NotFound
    },
    520486915: {
        '*': ae.AuthenticationFailure
    },
    520749062: {
        '*': ae.NotFound
    },
    654311465: {
        '*': ae.AddressSpecifiedIsInUse
    },
    654311495: {
        '*': ae.InUse,
    },
    654311496: {
        '*': ae.AddressSpecifiedIsInUse
    },
    654376968: {
        'nat.pool.delete': None,
        '*': ae.NotFound
    },
    654573574: {
        'network.acl.ext.delete': None,
        '*': ae.NotFound
    }
}


def raise_axapi_ex(response, action=None):
    if 'response' in response and 'err' in response['response']:
        code = response['response']['err']['code']

        if code in RESPONSE_CODES:
            ex_dict = RESPONSE_CODES[code]

            if action is not None and action in ex_dict:
                ex = ex_dict[action]
            else:
                ex = ex_dict.get('*')

            if ex is not None:
                raise ex(code, response['response']['err']['msg'])
            else:
                return

        raise ae.ACOSException(code, response['response']['err']['msg'])
    raise ae.ACOSException()
