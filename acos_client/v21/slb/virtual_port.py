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

from acos_client.v21 import base


class VirtualPort(base.BaseV21):

    # Protocols
    TCP = 2
    UDP = 3
    HTTP = 11
    HTTPS = 12
    OTHERS = 4
    RTSP = 5
    FTP = 6
    MMS = 7
    SIP = 8
    FAST_HTTP = 9
    GENERIC_PROXY = 10
    SSL_PROXY = 13
    SMTP = 14
    SIP_TCP = 15
    SIPS = 16
    DIAMETER = 17
    DNS_UDP = 18
    TFTP = 19
    DNS_TCP = 20
    RADIUS = 21
    MYSQL = 22
    MSSQL = 23
    FIX = 24
    SMPP_TCP = 25
    SPDY = 26
    SPDYS = 27
    FTP_PROXY = 28

    # The keys as specified in the ACOS JSON message.
    CLIENT_SSL_TMPL_KEY = "client_ssl_template"
    SERVER_SSL_TMPL_KEY = "server_ssl_template"

    # The keys as sent from a10-neutron-lbaas
    # They match what we use in v4 so we transform here
    CLIENT_SSL_ANL_KEY = "template_client_ssl"
    SERVER_SSL_ANL_KEY = "template_server_ssl"

    def _set(self, action, virtual_server_name, name, protocol, port,
             service_group_name,
             s_pers_name=None, c_pers_name=None, status=1,
             autosnat=False,
             ipinip=False,
             source_nat=None,
             **kwargs):
        params = {
            "name": virtual_server_name,
            "vport": self.minimal_dict({
                "name": name,
                "service_group": service_group_name,
                "protocol": protocol,
                "port": int(port),
                "source_ip_persistence_template": s_pers_name,
                "cookie_persistence_template": c_pers_name,
                "status": status
            })
        }

        client_ssl_template = kwargs.get(self.CLIENT_SSL_TMPL_KEY)
        server_ssl_template = kwargs.get(self.SERVER_SSL_TMPL_KEY)

        if client_ssl_template:
            params['vport'][self.CLIENT_SSL_ANL_KEY] = client_ssl_template

        if server_ssl_template:
            params['vport'][self.SERVER_SSL_ANL_KEY] = server_ssl_template

        if autosnat:
            params['vport']['source_nat_auto'] = int(autosnat)
        if ipinip:
            params['vport']['ip_in_ip'] = int(ipinip)
        if source_nat and len(source_nat) > 0:
            params['vport']['source_nat'] = source_nat

        self._post(action, params, **kwargs)

    def get(self, virtual_server_name, name, protocol, port, **kwargs):
        # There is no slb.virtual_server.vport.search.
        # Instead, we get the virtual server and get the desired vport.
        results = self._post('slb.virtual_server.search', {'name': virtual_server_name}, **kwargs)

        vports = results.get("virtual_server").get("vport_list", [])
        port_filter = lambda x: x.get("name") == name
        filtered_vports = [vport for vport in vports if port_filter(vport)]
        if len(filtered_vports) > 0:
            return filtered_vports[0]

    def create(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1,
               autosnat=False,
               ipinip=False,
               source_nat_pool=None,
               **kwargs):
        self._set('slb.virtual_server.vport.create', virtual_server_name,
                  name, protocol, port, service_group_name,
                  s_pers_name, c_pers_name, status,
                  autosnat=autosnat, ipinip=ipinip, source_nat=source_nat_pool,
                  **kwargs)

    def update(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1,
               autosnat=False,
               ipinip=False,
               source_nat_pool=None,
               **kwargs):
            self._set('slb.virtual_server.vport.update', virtual_server_name,
                      name, protocol, port, service_group_name,
                      s_pers_name, c_pers_name, status,
                      autosnat=autosnat, ipinip=ipinip, source_nat=source_nat_pool,
                      **kwargs)

    def delete(self, virtual_server_name, name, protocol, port, **kwargs):
        params = {
            "name": virtual_server_name,
            "vport": {
                "name": name,
                "protocol": protocol,
                "port": int(port)
            }
        }
        self._post("slb.virtual_server.vport.delete", params, **kwargs)
