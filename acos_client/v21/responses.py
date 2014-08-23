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
    1163: {
        '*': ae.InvalidParameter
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
    2941: {
        '*': ae.Exists
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
        '*': ae.NotFound
    },
    67239937: {
        'slb.virtual_server.delete': None,
        'slb.virtual_service.delete': None,
        '*': ae.NotFound
    },
    67239947: {
        '*': ae.Exists
    },
    67305473: {
        'slb.service_group.delete': None,
        'slb.service_group.member.create': ae.NoSuchServiceGroup,
        'slb.service_group.member.update': ae.NoSuchServiceGroup,
        '*': ae.NotFound
    },
    67371009: {
        'slb.template.cookie_persistence.delete': None,
        'slb.template.src_ip_persistence.delete': None,
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
}
