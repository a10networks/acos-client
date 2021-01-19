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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as ae
from acos_client.v30 import base


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

    def format_vport_url(self, port_number, protocol):
        if protocol == 'TERMINATED_HTTPS':
            protocol = "https"
        return self.url_port_tmpl.format(port_number=port_number, protocol=protocol)

    def all(self, virtual_server_name, **kwargs):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        return self._get(url, **kwargs)

    def get(self, virtual_server_name, name, protocol, port):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        url += self.format_vport_url(port_number=port, protocol=protocol)
        return self._get(url)

    def _set(
        self,
        virtual_server_name,
        name,
        protocol,
        protocol_port,
        service_group_name,
        s_pers_name=None,
        c_pers_name=None,
        status=0,
        no_dest_nat=None,
        autosnat=None,
        ipinip=None,
        source_nat_pool=None,
        ha_conn_mirror=None,
        use_rcv_hop=None,
        conn_limit=None,
        virtual_port_templates=None,
        tcp_template=None,
        udp_template=None,
        exclude_minimize=None,
        update=False,
        template_server_ssl=None,
        template_client_ssl=None,
        sampling_enable=None,
        aflex_scripts=None,
        **kwargs
    ):
        exclude_minimize = [] if exclude_minimize is None else exclude_minimize
        params = {
            "port": self.minimal_dict({
                "name": name,
                "service-group": service_group_name,
                "protocol": protocol,
                "port-number": int(protocol_port),
                "template-persist-source-ip": s_pers_name,
                "template-persist-cookie": c_pers_name,
                "extended-stats": status
            }, exclude=exclude_minimize
            )
        }
        if virtual_port_templates:
            virtual_port_templates = {k: v for k, v in virtual_port_templates.items() if v}

            if virtual_port_templates.get('template-virtual-port'):
                params['port']['template-virtual-port'] = virtual_port_templates['template-virtual-port']
            elif virtual_port_templates.get('template-virtual-port-shared'):
                params['port']['template-virtual-port-shared'] = virtual_port_templates['template-virtual-port-shared']
                params['port']['shared-partition-virtual-port-template'] = True

            if protocol in ['http', 'https']:
                if virtual_port_templates.get('template-http'):
                    params['port']['template-http'] = virtual_port_templates['template-http']
                elif virtual_port_templates.get('template-http-shared'):
                    params['port']['template-http-shared'] = virtual_port_templates['template-http-shared']
                    params['port']['shared-partition-http-template'] = True
            else:
                if virtual_port_templates.get('template-tcp'):
                    params['port']['template-tcp'] = virtual_port_templates['template-tcp']
                elif virtual_port_templates.get('template-tcp-shared'):
                    params['port']['template-tcp-shared'] = virtual_port_templates['template-tcp-shared']
                    params['port']['shared-partition-tcp'] = True

            if virtual_port_templates.get('template-policy'):
                params['port']['template-policy'] = virtual_port_templates['template-policy']
            elif virtual_port_templates.get('template-policy-shared'):
                params['port']['template-policy-shared'] = virtual_port_templates['template-policy-shared']
                params['port']['shared-partition-policy-template'] = True

        if autosnat is not None:
            params['port']['auto'] = int(autosnat)
        if ipinip is not None:
            params['port']['ipinip'] = int(ipinip)
        if use_rcv_hop is not None:
            params['port']['use-rcv-hop-for-resp'] = int(use_rcv_hop)

        if source_nat_pool and len(source_nat_pool) > 0:
            params['port']['pool'] = source_nat_pool
        if tcp_template:
            params['port']['tcp_template'] = tcp_template
        if udp_template:
            params['port']['udp_template'] = udp_template

        if template_server_ssl:
            params['port']['template-server-ssl'] = template_server_ssl
        if template_client_ssl:
            params['port']['template-client-ssl'] = template_client_ssl

        if sampling_enable is not None:
            self._set_sampling_enable(sampling_enable, params)

        if no_dest_nat is not None:
            params["port"]["no-dest-nat"] = 1 if no_dest_nat else 0
        if ha_conn_mirror is not None:
            if (protocol == self.TCP or protocol == self.UDP):
                params["port"]["ha-conn-mirror"] = 1 if ha_conn_mirror else 0
        if conn_limit is not None:
            params["port"]["conn-limit"] = conn_limit

        url = self.url_server_tmpl.format(name=virtual_server_name)

        if aflex_scripts is not None:
            params['port']['aflex-scripts'] = aflex_scripts

        if update:
            url += self.format_vport_url(port_number=protocol_port, protocol=protocol)
        return url, params, kwargs

    def create(
        self,
        virtual_server_name,
        name,
        protocol,
        protocol_port,
        service_group_name,
        s_pers_name=None,
        c_pers_name=None,
        status=1,
        autosnat=None,
        ipinip=None,
        no_dest_nat=None,
        source_nat_pool=None,
        ha_conn_mirror=None,
        use_rcv_hop=None,
        conn_limit=None,
        virtual_port_templates=None,
        tcp_template=None,
        udp_template=None,
        max_retries=None,
        timeout=None,
        template_server_ssl=None,
        template_client_ssl=None,
        sampling_enable=None,
        aflex_scripts=None,
        **kwargs
    ):

        # backward compatiable for a10-neutron-lbaas
        if aflex_scripts is None and 'aflex-scripts' in kwargs:
            aflex_scripts = kwargs.pop('aflex-scripts')

        url, params, kwargs = self._set(
            virtual_server_name,
            name,
            protocol,
            protocol_port,
            service_group_name,
            s_pers_name,
            c_pers_name,
            status,
            autosnat=autosnat,
            ipinip=ipinip,
            no_dest_nat=no_dest_nat,
            source_nat_pool=source_nat_pool,
            ha_conn_mirror=ha_conn_mirror,
            use_rcv_hop=use_rcv_hop,
            conn_limit=conn_limit,
            virtual_port_templates=virtual_port_templates,
            tcp_template=tcp_template,
            udp_template=udp_template,
            template_server_ssl=template_server_ssl,
            template_client_ssl=template_client_ssl,
            sampling_enable=sampling_enable,
            aflex_scripts=aflex_scripts,
            **kwargs
        )

        return self._post(url, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def _update(
        self,
        virtual_server_name,
        name,
        protocol,
        protocol_port,
        service_group_name,
        s_pers_name=None,
        c_pers_name=None,
        status=1,
        autosnat=None,
        ipinip=None,
        no_dest_nat=None,
        source_nat_pool=None,
        ha_conn_mirror=None,
        use_rcv_hop=None,
        conn_limit=None,
        virtual_port_templates=None,
        tcp_template=None,
        udp_template=None,
        template_server_ssl=None,
        template_client_ssl=None,
        sampling_enable=None,
        aflex_scripts=None,
        **kwargs
    ):

        vp = self.get(virtual_server_name, name, protocol, protocol_port)
        if vp is None:
            raise ae.NotFound()

        exclude = ['template-persist-source-ip', 'template-persist-cookie']

        try:
            url, params, kwargs = self._set(
                virtual_server_name,
                name,
                protocol,
                protocol_port,
                service_group_name,
                s_pers_name,
                c_pers_name,
                status,
                autosnat=autosnat,
                ipinip=ipinip,
                no_dest_nat=no_dest_nat,
                source_nat_pool=source_nat_pool,
                ha_conn_mirror=ha_conn_mirror,
                use_rcv_hop=use_rcv_hop,
                conn_limit=conn_limit,
                virtual_port_templates=virtual_port_templates,
                tcp_template=tcp_template,
                udp_template=udp_template,
                exclude_minimize=exclude,
                update=True,
                template_server_ssl=template_server_ssl,
                template_client_ssl=template_client_ssl,
                sampling_enable=sampling_enable,
                aflex_scripts=aflex_scripts,
                **kwargs
            )
        except ae.AxapiJsonFormatError:
            url, params, kwargs = self._set(
                virtual_server_name,
                name,
                protocol,
                protocol_port,
                service_group_name,
                s_pers_name,
                c_pers_name,
                status,
                autosnat=autosnat,
                ipinip=ipinip,
                no_dest_nat=no_dest_nat,
                source_nat_pool=source_nat_pool,
                ha_conn_mirror=ha_conn_mirror,
                use_rcv_hop=use_rcv_hop,
                conn_limit=conn_limit,
                virtual_port_templates=virtual_port_templates,
                tcp_template=tcp_template,
                udp_template=udp_template,
                exclude_minimize=exclude,
                update=True,
                template_server_ssl=template_server_ssl,
                template_client_ssl=template_client_ssl,
                sampling_enable=sampling_enable,
                aflex_scripts=aflex_scripts,
                **kwargs
            )
        return url, params, kwargs

    def update(
        self,
        virtual_server_name,
        name,
        protocol,
        protocol_port,
        service_group_name,
        s_pers_name=None,
        c_pers_name=None,
        status=1,
        autosnat=None,
        ipinip=None,
        no_dest_nat=None,
        source_nat_pool=None,
        ha_conn_mirror=None,
        use_rcv_hop=None,
        conn_limit=None,
        virtual_port_templates=None,
        tcp_template=None,
        udp_template=None,
        max_retries=None,
        timeout=None,
        template_server_ssl=None,
        template_client_ssl=None,
        sampling_enable=None,
        aflex_scripts=None,
        **kwargs
    ):

        # backward compatiable for a10-neutron-lbaas
        if aflex_scripts is None and 'aflex-scripts' in kwargs:
            aflex_scripts = kwargs.pop('aflex-scripts')

        url, params, kwargs = self._update(
            virtual_server_name,
            name,
            protocol,
            protocol_port,
            service_group_name,
            s_pers_name=s_pers_name,
            c_pers_name=c_pers_name,
            status=status,
            autosnat=autosnat,
            ipinip=ipinip,
            no_dest_nat=no_dest_nat,
            source_nat_pool=source_nat_pool,
            ha_conn_mirror=ha_conn_mirror,
            use_rcv_hop=use_rcv_hop,
            conn_limit=conn_limit,
            virtual_port_templates=virtual_port_templates,
            tcp_template=tcp_template,
            udp_template=udp_template,
            template_server_ssl=template_server_ssl,
            template_client_ssl=template_client_ssl,
            sampling_enable=sampling_enable,
            aflex_scripts=aflex_scripts,
            **kwargs)
        return self._post(url, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def replace(
        self,
        virtual_server_name,
        name,
        protocol,
        protocol_port,
        service_group_name,
        s_pers_name=None,
        c_pers_name=None,
        status=1,
        autosnat=None,
        ipinip=None,
        no_dest_nat=None,
        source_nat_pool=None,
        ha_conn_mirror=None,
        use_rcv_hop=None,
        conn_limit=None,
        virtual_port_templates=None,
        tcp_template=None,
        udp_template=None,
        max_retries=None,
        timeout=None,
        template_server_ssl=None,
        template_client_ssl=None,
        sampling_enable=None,
        aflex_scripts=None,
        **kwargs
    ):

        # backward compatiable for a10-neutron-lbaas
        if aflex_scripts is None and 'aflex-scripts' in kwargs:
            aflex_scripts = kwargs.pop('aflex-scripts')

        url, params, kwargs = self._update(
            virtual_server_name,
            name,
            protocol,
            protocol_port,
            service_group_name,
            s_pers_name=s_pers_name,
            c_pers_name=c_pers_name,
            status=status,
            autosnat=autosnat,
            ipinip=ipinip,
            no_dest_nat=no_dest_nat,
            source_nat_pool=source_nat_pool,
            ha_conn_mirror=ha_conn_mirror,
            use_rcv_hop=use_rcv_hop,
            conn_limit=conn_limit,
            virtual_port_templates=virtual_port_templates,
            tcp_template=tcp_template,
            udp_template=udp_template,
            template_server_ssl=template_server_ssl,
            template_client_ssl=template_client_ssl,
            sampling_enable=sampling_enable,
            aflex_scripts=aflex_scripts,
            **kwargs)
        return self._put(url, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def delete(self, virtual_server_name, name, protocol, port):
        url = self.url_server_tmpl.format(name=virtual_server_name)
        url += self.format_vport_url(port_number=port, protocol=protocol)
        return self._delete(url)

    def _set_sampling_enable(self, sample_list, dest_obj):
        dest_array = []
        for x in sample_list:
            entry = {"counters1": x}
            dest_array.append(entry)

        dest_obj["port"]["sampling-enable"] = dest_array
