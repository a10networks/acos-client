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

import acos_client.errors as ae
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

    def get(self, virtual_server_name, name, protocol, port):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        url += self.url_port_tmpl.format(
            port_number=port, protocol=protocol
        )
        return self._get(url)

    def _set(self, virtual_server_name, name, protocol, port,
             service_group_name,
             s_pers_name=None, c_pers_name=None, stats=0, update=False,
             no_dest_nat=None,
             exclude_minimize=[],
             autosnat=False,
             ipinip=False,
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
            }, exclude=exclude_minimize)
        }
        if autosnat:
            params['port']['auto'] = int(autosnat)
        if ipinip:
            params['port']['ipinip'] = int(ipinip)

        sampling_enable = kwargs.get('sampling_enable')
        if sampling_enable is not None:
            self._set_sampling_enable(sampling_enable, params)

        if no_dest_nat is not None:
            params["port"]["no-dest-nat"] = 1 if no_dest_nat else 0

        url = self.url_server_tmpl.format(name=virtual_server_name)
        if update:
            url += self.url_port_tmpl.format(
                port_number=port, protocol=protocol
            )

        return self._post(url, params, **kwargs)

    def create(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1,
               autosnat=False,
               ipinip=False,
               no_dest_nat=None, **kwargs):
        return self._set(virtual_server_name,
                         name, protocol, port, service_group_name,
                         s_pers_name, c_pers_name, status,
                         autosnat=autosnat, ipinip=ipinip,
                         no_dest_nat=no_dest_nat, **kwargs)

    def update(self, virtual_server_name, name, protocol, port,
               service_group_name,
               s_pers_name=None, c_pers_name=None, status=1,
               autosnat=False,
               ipinip=False,
               no_dest_nat=None, **kwargs):
        vp = self.get(virtual_server_name, name, protocol, port)
        if vp is None:
            raise ae.NotFound()

        exclu = ['template-persist-source-ip', 'template-persist-cookie']

        try:
            return self._set(virtual_server_name,
                             name, protocol, port, service_group_name,
                             s_pers_name, c_pers_name, status, True,
                             autosnat=autosnat, ipinip=ipinip,
                             exclude_minimize=exclu, no_dest_nat=no_dest_nat,
                             **kwargs)
        except ae.AxapiJsonFormatError:
            return self._set(virtual_server_name,
                             name, protocol, port, service_group_name,
                             s_pers_name, c_pers_name, status, True,
                             autosnat=autosnat, ipinip=ipinip,
                             exclude_minimize=[], no_dest_nat=no_dest_nat,
                             **kwargs)

    def delete(self, virtual_server_name, name, protocol, port):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        url += self.url_port_tmpl.format(port_number=port, protocol=protocol)
        return self._delete(url)

    def _set_sampling_enable(self, sample_list, dest_obj):
        dest_array = []
        for x in sample_list:
            entry = {"counters1": x}
            dest_array.append(entry)

        dest_obj["port"]["sampling-enable"] = dest_array
