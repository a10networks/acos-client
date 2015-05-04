# Copyright 2014,  Jeff Buttars,  A10 Networks.
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

import acos_client.v30.base as base


class VirtualPort(base.BaseV30):

    # Protocols
    TCP = "tcp"
    UDP = "udp"
    OTHERS = "others"
    DIAMETER = "diameter"
    DNS_TCP = "dns-tcp"
    DNS_UDP = "dns-udp"
    FAST_HTTP = "fast-http"
    FIX = "fix"
    FTP = "ftp"
    FTP_PROXY = "ftp-proxy"
    HTTP = "http"
    HTTPS = "https"
    MLB = "mlb"
    MMS = "mms"
    MYSQL = "mysql"
    MSSQL = "mssql"
    RADIUS = "radius"
    RTSP = "rtsp"
    SIP = "sip"
    SIP_TCP = "sip-tcp"
    SIPS = "sips"
    SMPP_TCP = "smpp-tcp"
    SPDY = "spdy"
    SPDYS = "spdys"
    SMTP = "smtp"
    SSL_PROXY = "ssl-proxy"
    TCP_PROXY = "tcp-proxy"
    TFTP = "tftp"
    GENERIC_PROXY = "tcp-proxy"

    url_server_tmpl = '/slb/virtual-server/{name}/port/'
    url_port_tmpl = '{port_number}+{protocol}'

    def all(self, virtual_server_name, **kwargs):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        return self._get(url, **kwargs)

    def _set(self, virtual_server_name, name, protocol, port,
             service_group_name,
             s_pers_name=None, c_pers_name=None, stats=0, update=False,
             **kwargs):

        params = {
            "port": self.minimal_dict({
                "name": name,
                "service-group": service_group_name,
                "protocol": protocol,
                "port-number": int(port),
                "template-persist-source-ip": s_pers_name,
                "template-persist-cookie": c_pers_name,
                "extended-stats": stats
            }, exclude=['template-persist-source-ip', 'template-persist-cookie'])
        }

        url = self.url_server_tmpl.format(name=virtual_server_name)
        if update:
            url += self.url_port_tmpl.format(
                port_number=port, protocol=protocol
            )

        return self._post(url, params, **kwargs)

    def create(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1, **kwargs):
        return self._set(virtual_server_name,
                         name, protocol, port, service_group_name,
                         s_pers_name, c_pers_name, status, **kwargs)

    def update(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1, **kwargs):
        return self._set(virtual_server_name,
                         name, protocol, port, service_group_name,
                         s_pers_name, c_pers_name, status, True, **kwargs)

    def delete(self, virtual_server_name, name, protocol, port):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        url += self.url_port_tmpl.format(port_number=port, protocol=protocol)
        return self._delete(url)
