# Copyright 2014-2016, A10 Networks.
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
import six


from acos_client import errors as acos_errors
from acos_client.v30 import base
from acos_client.v30.slb.virtual_port import VirtualPort


class VirtualServer(base.BaseV30):
    url_prefix = '/slb/virtual-server/'

    @property
    def vport(self):
        return VirtualPort(self.client)

    def all(self):
        return self._get(self.url_prefix)

    def get(self, name):
        return self._get(self.url_prefix + name)

    def _set(self, name, ip_address=None, arp_disable=False, vrid=None,
             virtual_server_templates=None, template_virtual_server=None, update=False, **kwargs):
        params = {
            "virtual-server": self.minimal_dict({
                "name": name,
                "ip-address": ip_address,
                "arp-disable": None if arp_disable is None else int(arp_disable)
            }),
        }
        if self._is_ipv6(ip_address):
            params['virtual-server']['ipv6-address'] = ip_address
        else:
            params['virtual-server']['ip-address'] = ip_address

        if vrid:
            params['virtual-server']['vrid'] = int(vrid)
        if virtual_server_templates:
            virtual_server_templates = {k: v for k, v in virtual_server_templates.items() if v}
            params['virtual-server']['template-virtual-server'] = \
                virtual_server_templates.get('template-virtual-server', None)
            params['virtual-server']['template-logging'] = virtual_server_templates.get('template-logging', None)
            params['virtual-server']['template-policy'] = virtual_server_templates.get('template-policy', None)
            params['virtual-server']['template-scaleout'] = virtual_server_templates.get('template-scaleout', None)

        # for backward compatibility
        if template_virtual_server:
            params['virtual-server']['template-virtual-server'] = str(template_virtual_server)

        config_defaults = kwargs.get("config_defaults")
        if config_defaults:
            for k, v in six.iteritems(config_defaults):
                params['virtual-server'][k] = v

        if not update:
            name = ''
        return self._post(self.url_prefix + name, params, **kwargs)

    def create(self, name, ip_address, arp_disable=False, vrid=None,
               virtual_server_templates=None, template_virtual_server=None, **kwargs):
        try:
            self.get(name)
        except acos_errors.NotFound:
            pass
        else:
            raise acos_errors.Exists

        return self._set(name, ip_address, arp_disable, vrid, virtual_server_templates,
                         template_virtual_server, **kwargs)

    def update(self, name, ip_address=None, arp_disable=False, vrid=None,
               virtual_server_templates=None, template_virtual_server=None, **kwargs):
        return self._set(name, ip_address, arp_disable, vrid, virtual_server_templates,
                         template_virtual_server, update=True, **kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)

    def stats(self, name='', **kwargs):
        resp = self._get(self.url_prefix + name + '/port/stats', **kwargs)
        return resp

    def oper(self, name='', **kwargs):
        resp = self._get(self.url_prefix + name + '/oper', **kwargs)
        return resp
